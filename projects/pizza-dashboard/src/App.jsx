import { useState } from 'react'
import './App.css'

const mockOrders = [
  { id: 1, customer: 'Ahmed', items: ['Margherita', 'Pepperoni'], total: 45, status: 'Delivered', time: '12:30 PM' },
  { id: 2, customer: 'Sara', items: ['BBQ Chicken'], total: 28, status: 'Preparing', time: '12:45 PM' },
  { id: 3, customer: 'Omar', items: ['Veggie Supreme', 'Garlic Bread'], total: 52, status: 'On the way', time: '1:00 PM' },
  { id: 4, customer: 'Fatima', items: ['Hawaiian'], total: 22, status: 'Pending', time: '1:15 PM' },
  { id: 5, customer: 'Khalid', items: ['Meat Lovers', 'Coke'], total: 38, status: 'Delivered', time: '11:50 AM' },
]

const popularPizzas = [
  { name: 'Margherita', orders: 142, revenue: 1988 },
  { name: 'Pepperoni', orders: 128, revenue: 2048 },
  { name: 'BBQ Chicken', orders: 95, revenue: 1710 },
  { name: 'Veggie Supreme', orders: 78, revenue: 1170 },
  { name: 'Hawaiian', orders: 64, revenue: 896 },
]

function StatCard({ title, value, icon, color }) {
  return (
    <div className="stat-card" style={{ borderLeft: `4px solid ${color}` }}>
      <div className="stat-icon">{icon}</div>
      <div className="stat-info">
        <h3>{title}</h3>
        <p>{value}</p>
      </div>
    </div>
  )
}

function StatusBadge({ status }) {
  const colors = {
    Delivered: '#22c55e',
    Preparing: '#f59e0b',
    'On the way': '#3b82f6',
    Pending: '#6b7280',
  }
  return <span className="status-badge" style={{ backgroundColor: colors[status] }}>{status}</span>
}

export default function App() {
  const [orders] = useState(mockOrders)

  const stats = {
    totalRevenue: '$7,812',
    totalOrders: '507',
    avgOrderValue: '$15.40',
    activeOrders: orders.filter(o => o.status !== 'Delivered').length,
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🍕 Pizza Palace Dashboard</h1>
        <p>Today's Overview</p>
      </header>

      <div className="stats-grid">
        <StatCard title="Total Revenue" value={stats.totalRevenue} icon="💰" color="#22c55e" />
        <StatCard title="Total Orders" value={stats.totalOrders} icon="📦" color="#3b82f6" />
        <StatCard title="Avg Order Value" value={stats.avgOrderValue} icon="📊" color="#8b5cf6" />
        <StatCard title="Active Orders" value={stats.activeOrders} icon="🔥" color="#f59e0b" />
      </div>

      <div className="dashboard-grid">
        <div className="card orders-card">
          <h2>Recent Orders</h2>
          <table>
            <thead>
              <tr>
                <th>Customer</th>
                <th>Items</th>
                <th>Total</th>
                <th>Status</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id}>
                  <td>{order.customer}</td>
                  <td>{order.items.join(', ')}</td>
                  <td>${order.total}</td>
                  <td><StatusBadge status={order.status} /></td>
                  <td>{order.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card popular-card">
          <h2>Popular Pizzas</h2>
          <ul>
            {popularPizzas.map((pizza, i) => (
              <li key={pizza.name}>
                <span className="rank">#{i + 1}</span>
                <span className="name">{pizza.name}</span>
                <span className="orders">{pizza.orders} orders</span>
                <span className="revenue">${pizza.revenue}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}
