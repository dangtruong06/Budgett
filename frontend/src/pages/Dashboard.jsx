import { useState, useEffect } from 'react'
import api from '../api/axios'
import { useNavigate, Link } from 'react-router-dom';
import Navbar from '../components/Navbar'
import { Pencil, Trash2, Plus } from 'lucide-react';

function Dashboard(){
    const [expenses, setExpenses] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchExpense = async () => {
            try{
                const response = await api.get('/expenses');
                setExpenses(response.data);
            }
            catch(error){
                console.error(error.response?.data);
            }
        };
        fetchExpense();
    }, [])

    const deleteExpense = async (id) => {
        try{
            await api.delete(`/expenses/${id}`);
            setExpenses(expenses.filter(expense => expense.id !== id));
        } catch(error){
            console.error(error.response?.data);
        }
    };
    
    const now = new Date();
    const monthlySpent = expenses
        .filter((e) => {
            const [year, month] = e.expense_date.split('-');
            return (
                Number(month) - 1 === now.getMonth() &&
                Number(year) === now.getFullYear()
            );
        })
        .reduce((sum, e) => sum + Number(e.amount), 0);

    const topCategory = (() => {
        if (expenses.length === 0) return '—';
        const totals = {};
        expenses.forEach((e) => {
            totals[e.category] = (totals[e.category] || 0) + Number(e.amount);
        });
        return Object.entries(totals).sort((a, b) => b[1] - a[1])[0][0];
    })();

    return (
        <div className="min-h-screen flex flex-col bg-emerald-50">
            <Navbar />
            <div className="flex-1 px-6 md:px-16 py-10 max-w-6xl mx-auto w-full">

                {/* Summary strip */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
                    <div className="bg-emerald-100 border border-emerald-200 rounded-2xl p-5">
                        <p className="text-sm text-gray-500 mb-2">Spent this month</p>
                        <p className="text-2xl font-medium text-gray-900">${monthlySpent.toFixed(2)}</p>
                    </div>
                    <div className="bg-emerald-100 border border-emerald-200 rounded-2xl p-5">
                        <p className="text-sm text-gray-500 mb-2">Entries</p>
                        <p className="text-2xl font-medium text-gray-900">{expenses.length}</p>
                    </div>
                    <div className="bg-emerald-100 border border-emerald-200 rounded-2xl p-5">
                        <p className="text-sm text-gray-500 mb-2">Top category</p>
                        <p className="text-2xl font-medium text-gray-900">{topCategory}</p>
                    </div>
                </div>

                {/* List header */}
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-lg font-medium text-gray-900">Recent expenses</h2>
                    <Link
                        to="/expenses/new"
                        className="flex items-center gap-1 px-4 py-2 text-sm font-medium text-white bg-emerald-600 rounded-lg hover:bg-emerald-700"
                    >
                        <Plus size={16} />
                        Add expense
                    </Link>
                </div>

                {expenses.length === 0 ? (
                    <div className="bg-white rounded-2xl border border-emerald-100 p-10 text-center">
                        <p className="text-gray-500 text-sm">
                            No expenses yet. Add your first one to get started.
                        </p>
                    </div>
                ) : (
                    <ul className="flex flex-col gap-3">
                        {expenses.map((expense) => (
                            <li
                                key={expense.id}
                                className="flex items-center justify-between bg-white rounded-2xl border border-emerald-100 px-5 py-4"
                            >
                                <div>
                                    <p className="font-medium text-gray-900">{expense.name}</p>
                                    <div className="flex items-center gap-2 text-xs text-gray-500 mt-1">
                                        <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 rounded-full">
                                            {expense.category}
                                        </span>
                                        <span>{expense.expense_date}</span>
                                    </div>
                                </div>
                                <div className="flex items-center gap-4">
                                    <span className="font-medium text-gray-900">
                                        ${Number(expense.amount).toFixed(2)}
                                    </span>
                                    <div className="flex items-center gap-2">
                                        <button
                                            onClick={() => navigate(`/expenses/${expense.id}/edit`)}
                                            className="p-2 text-gray-400 hover:text-emerald-600"
                                        >
                                            <Pencil size={16} />
                                        </button>
                                        <button
                                            onClick={() => deleteExpense(expense.id)}
                                            className="p-2 text-gray-400 hover:text-red-500"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    )
}

export default Dashboard;