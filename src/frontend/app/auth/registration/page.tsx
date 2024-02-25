"use client";
import { useState } from 'react';
import { proceedRegistration } from "@/components/ApiHandler";
import { UseAppContext } from '@/context';

export default function Registration() {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
    });

    const [errorData, setErrorData] = useState("");
    const [successData, setSuccessData] = useState("");
    const { actions } = UseAppContext();

    const handleChange = (e: any) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e: any) => {
        e.preventDefault();
        setSuccessData("");
        setErrorData("");

        actions.register(formData).then(setSuccessData).catch(setErrorData);
    };

    return (
        <div className="container d-flex justify-content-center align-items-center" style={{ height: '80vh' }}>
            <div className='card s21-card p-4 col-md-8 col-lg-6 col-xl-4 col-10'>
                <h3 className='card-title text-center'>Registration</h3>
                <div className='card-body text-center'>
                    <form onSubmit={handleSubmit}>
                        <div className="form-floating">
                            <input
                                type="email"
                                className="form-control"
                                placeholder="Leave a comment here"
                                name="email"
                                id="floatingTextarea"
                                onChange={handleChange}
                                required />
                            <label className="text-center" htmlFor="floatingTextarea">
                                Email
                            </label>
                        </div>
                        <div className="form-floating mt-3">
                            <input
                                type="text"
                                className="form-control"
                                placeholder="Leave a comment here"
                                name="username"
                                id="floatingTextarea"
                                onChange={handleChange}
                                required />
                            <label className="text-center" htmlFor="floatingTextarea">
                                Username
                            </label>
                        </div>
                        <div className="form-floating mt-3">
                            <input
                                type="password"
                                className="form-control"
                                placeholder="Leave a comment here"
                                name="password"
                                id="floatingTextarea"
                                onChange={handleChange}
                                required />
                            <label className="text-center" htmlFor="floatingTextarea">
                                Password
                            </label>
                        </div>
                        {
                            errorData?.length > 0 && (
                                <div className="alert alert-danger mt-3" role="alert">
                                    {errorData}
                                </div>
                            )
                        }
                        {
                            successData?.length > 0 && (
                                <div className="alert alert-success mt-3" role="alert">
                                    {successData}
                                </div>
                            )
                        }
                        {
                            successData?.length == 0 && (
                                <div className='row mt-3'>
                                    <div className='col text-center'>
                                        <button type='submit' className='btn s21-btn w-100' style={{ height: "55px" }}>
                                            Sign up
                                        </button>
                                    </div>
                                </div>
                            )
                        }
                    </form>
                </div>
                {
                    successData?.length == 0 && (
                        <div className='mt-3 text-center'>
                            <h5>Already have an account?</h5>
                            <div className='col text-center mt-3'>
                                <a href="/auth/login">
                                    <button type='button' className='btn s21-subbtn' style={{ height: "55px" }}>
                                        Sigh in
                                    </button>
                                </a>
                            </div>
                        </div>
                    )
                }
                {
                    successData.length > 0 && (
                        <div className='col text-center'>
                            <a href="/auth/login">
                                <button type='button' className='btn s21-subbtn' style={{ height: "55px" }}>
                                    Sigh in
                                </button>
                            </a>
                        </div>
                    )
                }
            </div>
        </div>
    );
}

// 