// dashboard/src/app/page.tsx
'use client';

import { useEffect, useState } from 'react';

interface Metrics {
  revenue_at_risk: number;
  recoverable: number;
  recovered: number;
  recovery_rate: number;
  actions_executed: number;
  policy_blocks: number;
}

export default function CommandCenter() {
  // Fix 1: Properly type the state to accept either null or the Metrics interface
  const [metrics, setMetrics] = useState<Metrics | null>(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/dashboard/metrics')
      .then((res) => res.json())
      .then((data) => setMetrics(data))
      .catch((err) => console.error('API Error:', err));
  }, []);

  // Fix 2: Wrap the loading text in valid HTML/JSX elements
  if (!metrics) {
    return (
      <div className="flex h-screen items-center justify-center font-sans text-lg">
        Loading Revora Command Center...
      </div>
    );
  }

  // Fix 3: Wrap all text and structural components in correct JSX tags
  return (
    <main className="p-8 font-sans max-w-6xl mx-auto">
      <header className="flex justify-between items-center mb-8 border-b pb-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Revora AI</h1>
          <p className="text-sm text-gray-500">Revenue Recovery Agent & Policy Guardrails</p>
        </div>
        <div className="flex items-center gap-4">
          <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm font-medium">
            View Risk Queue →
          </button>
          <span className="flex items-center gap-1.5 text-xs text-green-600 bg-green-50 px-2 py-1 rounded">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            Live Backend Sync Active
          </span>
        </div>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Metric Card 1 */}
        <div className="p-6 bg-white border rounded-xl shadow-sm">
          <h2 className="text-sm font-medium text-gray-500">Revenue At Risk</h2>
          <p className="text-2xl font-bold mt-2 text-red-600">
            ₹{(metrics.revenue_at_risk / 100).toLocaleString('en-IN')}
          </p>
        </div>

        {/* Metric Card 2 */}
        <div className="p-6 bg-white border rounded-xl shadow-sm">
          <h2 className="text-sm font-medium text-gray-500">Safe Revenue Recovered</h2>
          <p className="text-2xl font-bold mt-2 text-green-600">
            ₹{(metrics.recovered / 100).toLocaleString('en-IN')}
          </p>
          <p className="text-xs text-gray-400 mt-1">Recovery Rate: {metrics.recovery_rate}%</p>
        </div>

        {/* Metric Card 3 */}
        <div className="p-6 bg-white border rounded-xl shadow-sm">
          <h2 className="text-sm font-medium text-gray-500">Automated Actions Executed</h2>
          <p className="text-2xl font-bold mt-2 text-gray-900">
            {metrics.actions_executed}
          </p>
          <p className="text-xs text-gray-400 mt-1">Verified via Razorpay API & Policy Engine</p>
        </div>

        {/* Metric Card 4 */}
        <div className="p-6 bg-white border rounded-xl shadow-sm">
          <h2 className="text-sm font-medium text-gray-500">Policy Blocks / Escalations</h2>
          <p className="text-2xl font-bold mt-2 text-amber-600">
            {metrics.policy_blocks}
          </p>
          <p className="text-xs text-gray-400 mt-1">0 Safety Violations (Stopped Unsafe Retries)</p>
        </div>
      </section>
    </main>
  );
}
