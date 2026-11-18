const state = { customers: [], products: [], invoices: [], calculated: null };

const $ = (id) => document.getElementById(id);
const money = (value) => Number(value).toFixed(2);

function showView(name) {
  document.querySelectorAll(".view").forEach((view) => view.hidden = true);
  $(`${name}-view`).hidden = false;
  if (name === "invoices") refreshInvoiceOptions();
  refreshDashboard();
}

function refreshDashboard() {
  $("customer-count").textContent = state.customers.length;
  $("product-count").textContent = state.products.length;
  $("invoice-count").textContent = state.invoices.length;
}

function renderList(elementId, items, testId, formatter) {
  const container = $(elementId);
  container.innerHTML = "";
  items.forEach((item) => {
    const row = document.createElement("div");
    row.className = "row";
    row.dataset.testid = testId;
    row.textContent = formatter(item);
    container.appendChild(row);
  });
}

$("login-button").addEventListener("click", () => {
  const valid = $("username").value === "admin" && $("password").value === "admin123";
  $("login-error").textContent = valid ? "" : "Invalid username or password";
  if (valid) {
    $("login-view").hidden = true;
    $("erp-view").hidden = false;
    showView("dashboard");
  }
});

$("logout-button").addEventListener("click", () => {
  $("erp-view").hidden = true;
  $("login-view").hidden = false;
  $("password").value = "";
});

document.querySelectorAll("[data-view]").forEach((button) => {
  button.addEventListener("click", () => showView(button.dataset.view));
});

$("save-customer").addEventListener("click", () => {
  const name = $("customer-name").value.trim();
  const email = $("customer-email").value.trim();
  const phone = $("customer-phone").value.trim();
  $("customer-error").textContent = "";
  $("customer-success").textContent = "";
  if (!name) { $("customer-error").textContent = "Customer name is required"; return; }
  if (!email.includes("@")) { $("customer-error").textContent = "Enter a valid email"; return; }
  if (state.customers.some((customer) => customer.email === email)) {
    $("customer-error").textContent = "Customer email already exists"; return;
  }
  state.customers.push({ name, email, phone });
  $("customer-success").textContent = "Customer saved successfully";
  $("customer-name").value = $("customer-email").value = $("customer-phone").value = "";
  renderList("customer-list", state.customers, "customer-row",
    (customer) => `${customer.name} | ${customer.email} | ${customer.phone}`);
  refreshInvoiceOptions();
  refreshDashboard();
});

$("customer-search").addEventListener("input", (event) => {
  const query = event.target.value.toLowerCase();
  const filtered = state.customers.filter((customer) => customer.name.toLowerCase().includes(query));
  renderList("customer-list", filtered, "customer-row",
    (customer) => `${customer.name} | ${customer.email} | ${customer.phone}`);
});

$("save-product").addEventListener("click", () => {
  const name = $("product-name").value.trim();
  const sku = $("product-sku").value.trim();
  const price = Number($("product-price").value);
  const stock = Number($("product-stock").value);
  $("product-error").textContent = "";
  $("product-success").textContent = "";
  if (!name || !sku) { $("product-error").textContent = "Product name and SKU are required"; return; }
  if (!Number.isFinite(price) || price <= 0) { $("product-error").textContent = "Price must be greater than zero"; return; }
  if (!Number.isInteger(stock) || stock < 0) { $("product-error").textContent = "Stock must be a non-negative integer"; return; }
  if (state.products.some((product) => product.sku === sku)) {
    $("product-error").textContent = "SKU already exists"; return;
  }
  state.products.push({ name, sku, price, stock });
  $("product-success").textContent = "Product saved successfully";
  $("product-name").value = $("product-sku").value = $("product-price").value = $("product-stock").value = "";
  renderList("product-list", state.products, "product-row",
    (product) => `${product.name} | ${product.sku} | ₹${money(product.price)} | Stock: ${product.stock}`);
  refreshInvoiceOptions();
  refreshDashboard();
});

function refreshInvoiceOptions() {
  const customer = $("invoice-customer");
  const product = $("invoice-product");
  customer.innerHTML = '<option value="">Select customer</option>';
  product.innerHTML = '<option value="">Select product</option>';
  state.customers.forEach((item) => customer.add(new Option(item.name, item.email)));
  state.products.forEach((item) => product.add(new Option(item.name, item.sku)));
}

$("calculate-invoice").addEventListener("click", () => {
  $("invoice-error").textContent = "";
  const customer = state.customers.find((item) => item.email === $("invoice-customer").value);
  const product = state.products.find((item) => item.sku === $("invoice-product").value);
  const quantity = Number($("invoice-quantity").value);
  const gstRate = Number($("invoice-gst").value);
  if (!customer || !product) { $("invoice-error").textContent = "Select a customer and product"; return; }
  if (!Number.isInteger(quantity) || quantity <= 0) { $("invoice-error").textContent = "Quantity must be greater than zero"; return; }
  if (quantity > product.stock) { $("invoice-error").textContent = "Insufficient stock"; return; }
  const subtotal = product.price * quantity;
  const gst = subtotal * gstRate / 100;
  const total = subtotal + gst;
  state.calculated = { customer, product, quantity, gstRate, subtotal, gst, total };
  $("invoice-subtotal").textContent = money(subtotal);
  $("invoice-gst-amount").textContent = money(gst);
  $("invoice-total").textContent = money(total);
});

$("save-invoice").addEventListener("click", () => {
  $("invoice-error").textContent = "";
  $("invoice-success").textContent = "";
  if (!state.calculated) { $("invoice-error").textContent = "Calculate invoice before saving"; return; }
  const invoice = { ...state.calculated, number: `INV-${String(state.invoices.length + 1).padStart(4, "0")}` };
  invoice.product.stock -= invoice.quantity;
  state.invoices.push(invoice);
  state.calculated = null;
  $("invoice-success").textContent = `Invoice ${invoice.number} saved successfully`;
  renderList("invoice-list", state.invoices, "invoice-row",
    (item) => `${item.number} | ${item.customer.name} | ₹${money(item.total)}`);
  renderList("product-list", state.products, "product-row",
    (item) => `${item.name} | ${item.sku} | ₹${money(item.price)} | Stock: ${item.stock}`);
  refreshDashboard();
});
