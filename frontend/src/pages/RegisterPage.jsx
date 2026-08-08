import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/axios'
import Navbar from '../components/Navbar'

function RegisterPage(){
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const [error, setError] = useState('');

    const handleRegister = async (e) => {
        e.preventDefault()
        setError('');

        try{
            const response = await api.post('/register', { email, password });
            navigate('/login')
        }
        catch(error){
            setError(error.response?.data?.error || 'Something went wrong. Please try again.');     
        }
    };

    return (
        <div className="min-h-screen flex flex-col bg-emerald-50">
            <Navbar />
            <div className="flex-1 flex items-center justify-center px-4">
                <div className="w-full max-w-sm bg-white rounded-2xl p-8 shadow-sm border border-emerald-100">
                    <h1 className="text-xl font-medium text-gray-900 mb-6 text-center">
                        Create your account
                    </h1>
                    {error && (
                        <p className="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2 mb-4 text-center">
                            {error}
                        </p>
                    )}
                    <form onSubmit={handleRegister} className="flex flex-col gap-3">
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="email"
                            required
                            className="px-4 py-2 rounded-lg border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
                        />
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="password"
                            required
                            className="px-4 py-2 rounded-lg border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
                        />
                        <input
                            type="submit"
                            value="Sign up"
                            className="mt-2 px-4 py-2 rounded-lg bg-emerald-600 text-white text-sm font-medium hover:bg-emerald-700 cursor-pointer"
                        />
                    </form>
                    <p className="text-center text-sm text-gray-500 mt-6">
                        Already have an account?{' '}
                        <Link to="/login" className="text-emerald-700 font-medium hover:underline">
                            Log in
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    )
}

export default RegisterPage;