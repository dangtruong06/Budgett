import { useState, useEffect } from 'react'
import api from '../api/axios'
import { useNavigate } from 'react-router-dom';

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

    return (
        <div>
            <h2 className="text-2xl font-bold text-blue-600">Your expenses</h2>
            <ul>
                {expenses.map((expense) => (
                    <li key={expense.id}>
                        {expense.name} - {expense.amount} - {expense.category} - {expense.expense_date} 
                        <button onClick={() => navigate(`/expenses/${expense.id}/edit`)}>Edit</button>
                        <button onClick={ () => deleteExpense(expense.id) }>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default Dashboard;