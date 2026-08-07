import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../api/axios'

function ExpenseForm(){
    const { id } = useParams();
    const isEditMode = Boolean(id);
    const [name, setName] = useState('')
    const [category, setCategory] = useState('')
    const [amount, setAmount] = useState('')
    const [expenseDate, setExpenseDate] = useState('');
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
            console.error(error.response?.data);
        }
    };

    return (
        <form onSubmit={ handleSubmit }>
            <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Expense"/>
            <input value={amount} onChange={(e) => setAmount(e.target.value)} placeholder="12.35$" type="number"/>
            <input value={category} onChange={(e) => setCategory(e.target.value)} placeholder="Category"/>
            <input value={expenseDate} onChange={(e) => setExpenseDate(e.target.value)} type="date"/>
            <input type="submit" />
        </form>
    )
}

export default ExpenseForm;