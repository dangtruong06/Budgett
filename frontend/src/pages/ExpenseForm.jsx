import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../api/axios'
import Navbar from '../components/Navbar'

const CATEGORIES = ['Food', 'Transit', 'Housing', 'Utilities', 'Entertainment', 'Personal', 'Other'];

function ExpenseForm(){
    const { id } = useParams();
    const isEditMode = Boolean(id);
    const [name, setName] = useState('')
    const [category, setCategory] = useState('')
    const [amount, setAmount] = useState('')
    const [expenseDate, setExpenseDate] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        if (isEditMode){
            const fetchExpense = async () => {
                try{
                    const response = await api.get(`/expenses/${id}`);
                    setName(response.data.name);
                    setCategory(response.data.category);
                    setAmount(response.data.amount);
                    setExpenseDate(response.data.expense_date);
                } catch(error){
                    console.error(error.response?.data);
                }

            };

            fetchExpense();
        }
    }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try{
            if(isEditMode){
                await api.put(`/expenses/${id}`, {
                    name, category, amount, expense_date:expenseDate
                });
            }
            else{
                await api.post('/expenses', {
                    name, category, amount, expense_date:expenseDate
                })
            }

            navigate('/dashboard');
        } catch(error){
            setError(error.response?.data?.error || 'Something went wrong. Please try again.'); 
        }
    };

    return (
        <div className="min-h-screen flex flex-col bg-emerald-50">
            <Navbar />
            <div className="flex-1 flex items-center justify-center px-4 py-10">
                <div className="flex flex-col md:flex-row gap-6 w-full max-w-2xl">

                    {/* Form */}
                    <div className="flex-1 bg-white border border-emerald-100 rounded-2xl p-8">
                        <h1 className="text-lg font-medium text-gray-900 mb-5">
                            {isEditMode ? 'Edit expense' : 'Add expense'}
                        </h1>

                        {error && (
                            <p className="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2 mb-4">
                                {error}
                            </p>
                        )}

                        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
                            <input
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                placeholder="Expense name"
                                required
                                className="px-4 py-2 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
                            />
                            <input
                                value={amount}
                                onChange={(e) => setAmount(e.target.value)}
                                placeholder="0.00"
                                type="number"
                                step="0.01"
                                required
                                className="px-4 py-2 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
                            />
                            <select
                                value={category}
                                onChange={(e) => setCategory(e.target.value)}
                                required
                                className="px-4 py-2 rounded-lg border border-gray-200 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                            >
                                <option value="" disabled>Select a category</option>
                                {CATEGORIES.map((c) => (
                                    <option key={c} value={c}>{c}</option>
                                ))}
                            </select>
                            <input
                                value={expenseDate}
                                onChange={(e) => setExpenseDate(e.target.value)}
                                type="date"
                                required
                                className="px-4 py-2 rounded-lg border border-gray-200 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                            />
                            <button
                                type="submit"
                                className="mt-2 px-4 py-2 rounded-lg bg-emerald-600 text-white text-sm font-medium hover:bg-emerald-700"
                            >
                                Save expense
                            </button>
                        </form>
                    </div>

                    <div className="w-full md:w-56 bg-emerald-100 rounded-2xl p-6 flex flex-col items-center justify-center text-center">
                        <p className="text-xs text-emerald-700 mb-2">Preview</p>
                        <p className="text-2xl font-semibold text-emerald-900">
                            ${amount ? Number(amount).toFixed(2) : '0.00'}
                        </p>
                        <p className="text-sm text-emerald-800 mt-2">
                            {name || 'Expense name'}
                        </p>
                        {category && (
                            <span className="text-xs bg-white text-emerald-700 px-3 py-1 rounded-full mt-3">
                                {category}
                            </span>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ExpenseForm;