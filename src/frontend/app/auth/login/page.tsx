"use client";
import { UseAppContext } from '@/context';
import { useState } from 'react';
import { useRouter } from 'next/navigation';


export default function Login() {
    const [formData, setFormData] = useState({
        username: "",
        password: ""
    })
    const router = useRouter();
    const [errorData, setErrorData] = useState("");
    const { actions } = UseAppContext();

    const handleChange = (e: any) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e: any) => {
        e.preventDefault();
        setErrorData('');
        actions.login(formData)
            .then(() => router.push('/'))
            .catch((error: string) => setErrorData(error));
    };

    return (
        <div className="container d-flex justify-content-center align-items-center" style={{ height: '80vh' }}>
            <div className='card s21-card p-4 col-md-8 col-lg-6 col-xl-4 col-10'>
                <h3 className='card-title text-center'>Login</h3>
                <div className='card-body text-center'>
                    {
                        actions.isLoggedIn() ? (
                            <div className="alert alert-success mt-3">You are logged in!</div>
                        ) : (

                            <form onSubmit={handleSubmit}>
                                <div className="form-floating">
                                    <input
                                        type="text"
                                        className="form-control"
                                        placeholder="Leave a comment here"
                                        name='username'
                                        onChange={handleChange}
                                        id="floatingTextarea" />
                                    <label className="text-center" htmlFor="floatingTextarea">
                                        Username
                                    </label>
                                </div>
                                <div className="form-floating mt-3">
                                    <input
                                        type="password"
                                        className="form-control"
                                        placeholder="Leave a comment here"
                                        name='password'
                                        onChange={handleChange}
                                        id="floatingTextarea" />
                                    <label className="text-center" htmlFor="floatingTextarea">
                                        Password
                                    </label>
                                </div>
                                {errorData && (
                                    <div className="alert alert-danger mt-3" role="alert">
                                        {errorData}
                                    </div>
                                )}
                                <div className='row mt-3'>
                                    <div className='col text-center'>
                                        <button type='submit' className='btn s21-btn w-100' style={{ height: "55px" }}>
                                            Sign in
                                        </button>
                                    </div>
                                </div>
                                <div className='mt-3 text-center'>
                                    <h5>Do not have an account?</h5>
                                    <div className='row mt-3'>
                                        <div className='col text-center'>
                                            <a href="/auth/registration">
                                                <button type='button' className='btn s21-subbtn' style={{ height: "55px" }}>
                                                    Sign up
                                                </button>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        )
                    }
                </div>
            </div>
        </div>
    );

}
