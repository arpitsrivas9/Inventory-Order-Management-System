
import { useEffect, useState } from 'react'

const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

function App() {
  const [products, setProducts] = useState([])
  const [customers, setCustomers] = useState([])
  const [orders, setOrders] = useState([])
  const [productForm, setProductForm] = useState({ name: '', sku: '', price: '', stock: '' })
  const [customerForm, setCustomerForm] = useState({ name: '', email: '' })
  const [orderForm, setOrderForm] = useState({ customer_id: '', product_id: '', quantity: 1 })

  const refreshAll = async () => {
    const [productsRes, customersRes, ordersRes] = await Promise.all([
      fetch(`${apiBase}/products`),
      fetch(`${apiBase}/customers`),
      fetch(`${apiBase}/orders`),
    ])

    setProducts(await productsRes.json())
    setCustomers(await customersRes.json())
    setOrders(await ordersRes.json())
  }

  useEffect(() => {
    refreshAll()
  }, [])

  const addProduct = async () => {
    const res = await fetch(`${apiBase}/products`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: productForm.name,
        sku: productForm.sku,
        price: Number(productForm.price),
        stock: Number(productForm.stock),
      }),
    })
    if (res.ok) {
      setProductForm({ name: '', sku: '', price: '', stock: '' })
      refreshAll()
    } else {
      alert((await res.json()).detail || 'Failed to add product')
    }
  }

  const addCustomer = async () => {
    const res = await fetch(`${apiBase}/customers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: customerForm.name,
        email: customerForm.email,
      }),
    })
    if (res.ok) {
      setCustomerForm({ name: '', email: '' })
      refreshAll()
    } else {
      alert((await res.json()).detail || 'Failed to add customer')
    }
  }

  const createOrder = async () => {
    if (!orderForm.customer_id || !orderForm.product_id || orderForm.quantity < 1) {
      alert('Please select a customer, product and enter a valid quantity.')
      return
    }

    const res = await fetch(`${apiBase}/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        customer_id: Number(orderForm.customer_id),
        items: [
          {
            product_id: Number(orderForm.product_id),
            quantity: Number(orderForm.quantity),
          },
        ],
      }),
    })

    if (res.ok) {
      setOrderForm({ customer_id: '', product_id: '', quantity: 1 })
      refreshAll()
    } else {
      alert((await res.json()).detail || 'Failed to create order')
    }
  }

  return (
    <main>
      <h1>Inventory & Order Management System</h1>

      <section>
        <h2>Products</h2>
        <div className="form-group">
          <input
            placeholder="Name"
            value={productForm.name}
            onChange={(e) => setProductForm({ ...productForm, name: e.target.value })}
          />
          <input
            placeholder="SKU"
            value={productForm.sku}
            onChange={(e) => setProductForm({ ...productForm, sku: e.target.value })}
          />
          <input
            placeholder="Price"
            type="number"
            value={productForm.price}
            onChange={(e) => setProductForm({ ...productForm, price: e.target.value })}
          />
          <input
            placeholder="Stock"
            type="number"
            value={productForm.stock}
            onChange={(e) => setProductForm({ ...productForm, stock: e.target.value })}
          />
        </div>
        <button onClick={addProduct}>Add Product</button>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>SKU</th>
              <th>Price</th>
              <th>Stock</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id}>
                <td>{product.name}</td>
                <td>{product.sku}</td>
                <td>{product.price}</td>
                <td>{product.stock}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h2>Customers</h2>
        <div className="form-group">
          <input
            placeholder="Name"
            value={customerForm.name}
            onChange={(e) => setCustomerForm({ ...customerForm, name: e.target.value })}
          />
          <input
            placeholder="Email"
            type="email"
            value={customerForm.email}
            onChange={(e) => setCustomerForm({ ...customerForm, email: e.target.value })}
          />
        </div>
        <button onClick={addCustomer}>Add Customer</button>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
            </tr>
          </thead>
          <tbody>
            {customers.map((customer) => (
              <tr key={customer.id}>
                <td>{customer.name}</td>
                <td>{customer.email}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h2>Create Order</h2>
        <div className="form-group">
          <select
            value={orderForm.customer_id}
            onChange={(e) => setOrderForm({ ...orderForm, customer_id: e.target.value })}
          >
            <option value="">Select customer</option>
            {customers.map((customer) => (
              <option key={customer.id} value={customer.id}>
                {customer.name}
              </option>
            ))}
          </select>
          <select
            value={orderForm.product_id}
            onChange={(e) => setOrderForm({ ...orderForm, product_id: e.target.value })}
          >
            <option value="">Select product</option>
            {products.map((product) => (
              <option key={product.id} value={product.id}>
                {product.name} ({product.stock} in stock)
              </option>
            ))}
          </select>
          <input
            type="number"
            min="1"
            value={orderForm.quantity}
            onChange={(e) => setOrderForm({ ...orderForm, quantity: Number(e.target.value) })}
          />
        </div>
        <button onClick={createOrder}>Create Order</button>
      </section>

      <section>
        <h2>Orders</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer</th>
              <th>Total</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td>{order.id}</td>
                <td>{order.customer_name || order.customer_id}</td>
                <td>{order.total_amount}</td>
                <td>{new Date(order.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  )
}

export default App
