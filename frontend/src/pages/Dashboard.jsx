import { useState, useEffect } from 'react'
import api from '../api/axios'

function Dashboard(){
    const [expenses, setExpenses] = useState([]);

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

    return (
        <div>
            <h2>Your expenses</h2>
            <ul>
                {expenses.map((expense) => (
                    <li key={expense.id}>
                        {expense.name} - {expense.amount} - {expense.category} - {expense.expense_date}
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default Dashboard;