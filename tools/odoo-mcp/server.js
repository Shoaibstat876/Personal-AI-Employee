import fs from "fs";
import path from "path";
import dotenv from "dotenv";
import { fileURLToPath } from "url";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema
} from "@modelcontextprotocol/sdk/types.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({ path: path.resolve(__dirname, "../../.env.odoo") });

const ODOO_URL = process.env.ODOO_URL;
const ODOO_DB = process.env.ODOO_DB;
const ODOO_USER = process.env.ODOO_USER;
const ODOO_API_KEY = process.env.ODOO_API_KEY;

function requireEnv(name, value) {
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
}

requireEnv("ODOO_URL", ODOO_URL);
requireEnv("ODOO_DB", ODOO_DB);
requireEnv("ODOO_USER", ODOO_USER);
requireEnv("ODOO_API_KEY", ODOO_API_KEY);

async function jsonRpc(service, method, args) {
  const response = await fetch(`${ODOO_URL}/jsonrpc`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method: "call",
      params: {
        service,
        method,
        args
      },
      id: Date.now()
    })
  });

  const data = await response.json();
  if (data.error) {
    throw new Error(JSON.stringify(data.error, null, 2));
  }
  return data.result;
}

async function login() {
  const uid = await jsonRpc("common", "login", [
    ODOO_DB,
    ODOO_USER,
    ODOO_API_KEY
  ]);
  if (!uid) {
    throw new Error("Odoo login failed");
  }
  return uid;
}

async function executeKw(model, method, positionalArgs = [], keywordArgs = {}) {
  const uid = await login();
  return await jsonRpc("object", "execute_kw", [
    ODOO_DB,
    uid,
    ODOO_API_KEY,
    model,
    method,
    positionalArgs,
    keywordArgs
  ]);
}

async function listCustomers() {
  return await executeKw("res.partner", "search_read", [[]], {
    fields: ["id", "name", "email", "phone"],
    limit: 20
  });
}

async function createCustomer({ name, email = "", phone = "" }) {
  if (!name) throw new Error("name is required");
  const id = await executeKw("res.partner", "create", [
    {
      name,
      email,
      phone
    }
  ]);
  return { id, name, email, phone };
}

async function listInvoices() {
  return await executeKw("account.move", "search_read", [
    [["move_type", "=", "out_invoice"]]
  ], {
    fields: ["id", "name", "state", "amount_total", "invoice_date"],
    limit: 20
  });
}

async function createInvoice({ customer_name, product_name, quantity = 1 }) {
  if (!customer_name) throw new Error("customer_name is required");
  if (!product_name) throw new Error("product_name is required");

  const partners = await executeKw("res.partner", "search_read", [
    [["name", "=", customer_name]]
  ], {
    fields: ["id", "name"],
    limit: 1
  });

  if (!partners.length) {
    throw new Error(`Customer not found: ${customer_name}`);
  }

  const products = await executeKw("product.template", "search_read", [
    [["name", "=", product_name]]
  ], {
    fields: ["id", "name", "list_price"],
    limit: 1
  });

  if (!products.length) {
    throw new Error(`Product not found: ${product_name}`);
  }

  const partnerId = partners[0].id;
  const productTemplateId = products[0].id;

  const productVariants = await executeKw("product.product", "search_read", [
    [["product_tmpl_id", "=", productTemplateId]]
  ], {
    fields: ["id", "name"],
    limit: 1
  });

  if (!productVariants.length) {
    throw new Error(`No product variant found for: ${product_name}`);
  }

  const productId = productVariants[0].id;

  const invoiceId = await executeKw("account.move", "create", [
    {
      move_type: "out_invoice",
      partner_id: partnerId,
      invoice_line_ids: [
        [
          0,
          0,
          {
            product_id: productId,
            quantity
          }
        ]
      ]
    }
  ]);

  return {
    invoice_id: invoiceId,
    customer_name,
    product_name,
    quantity
  };
}

const server = new Server(
  {
    name: "odoo-mcp",
    version: "1.0.0"
  },
  {
    capabilities: {
      tools: {}
    }
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "list_customers",
        description: "List Odoo customers",
        inputSchema: {
          type: "object",
          properties: {}
        }
      },
      {
        name: "create_customer",
        description: "Create an Odoo customer",
        inputSchema: {
          type: "object",
          properties: {
            name: { type: "string" },
            email: { type: "string" },
            phone: { type: "string" }
          },
          required: ["name"]
        }
      },
      {
        name: "list_invoices",
        description: "List Odoo customer invoices",
        inputSchema: {
          type: "object",
          properties: {}
        }
      },
      {
        name: "create_invoice",
        description: "Create an Odoo customer invoice",
        inputSchema: {
          type: "object",
          properties: {
            customer_name: { type: "string" },
            product_name: { type: "string" },
            quantity: { type: "number" }
          },
          required: ["customer_name", "product_name"]
        }
      }
    ]
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args = {} } = request.params;

  try {
    let result;

    switch (name) {
      case "list_customers":
        result = await listCustomers();
        break;
      case "create_customer":
        result = await createCustomer(args);
        break;
      case "list_invoices":
        result = await listInvoices();
        break;
      case "create_invoice":
        result = await createInvoice(args);
        break;
      default:
        throw new Error(`Unknown tool: ${name}`);
    }

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2)
        }
      ]
    };
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`
        }
      ],
      isError: true
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);