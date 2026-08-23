import { useState } from 'react';
import api from '../api/axios'
import { useAuth } from '../context/AuthContext'
import { useNavigate, Link } from 'react-router-dom';
import Navbar from '../components/Navbar'
import { GoogleLogin } from '@react-oauth/google';

function LoginPage(){
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try{
            const response = await api.post('/login', { email, password }); 
            login(response.data.access_token);
            navigate('/dashboard')
            
        } catch (error){
            setError(error.response?.data?.error || 'Something went wrong. Please try again.');
        }

    };
    const handleGoogleSuccess = async (credentialResponse) => {
        setError('');
        try {
            const response = await api.post('/auth/google', {
                credential: credentialResponse.credential
            });
            login(response.data.access_token);
            navigate('/dashboard');
        } catch (error) {
            setError(error.response?.data?.error || 'Google sign-in failed. Please try again.');
        }
    };

    return (
        <div className="min-h-screen flex flex-col bg-emerald-50">
            <Navbar />
            <div className="flex-1 flex items-center justify-center px-4">
                <div className="w-full max-w-sm bg-white rounded-2xl p-8 shadow-sm border border-emerald-100">
                    <h1 className="text-xl font-medium text-gray-900 mb-6 text-center">
                        Log In
                    </h1>
                    {error && (
                        <p className="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2 mb-4 text-center">
                            {error}
                        </p>
                    )}
                    <form onSubmit={handleSubmit} className="flex flex-col gap-3">
                        <input 
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="email@email.com"
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
                        <button
                            type="submit"
                            className="mt-2 px-4 py-2 rounded-lg bg-emerald-600 text-white text-sm font-medium hover:bg-emerald-700"
                        >
                            Log In
                        </button>
                    </form>
                    <div className="mt-4 flex justify-center">
                        <GoogleLogin
                            onSuccess={handleGoogleSuccess}
                            onError={() => setError('Google sign-in failed. Please try again.')}
                        />
                    </div>
                    <p className="text-center text-sm text-gray-500 mt-6">
                        Don't have an account?{' '}
                        <Link to="/register" className="text-emerald-700 font-medium hover:underline">
                            Sign up
                        </Link>
                    </p>
                </div>
            </div>
        </div>



    );
}

export default LoginPage;