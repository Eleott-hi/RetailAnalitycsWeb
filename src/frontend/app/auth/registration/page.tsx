
export default async function Registration() {
    return (
        <div className="container bg-primary text-center">
            {/* <div className='card s21-card p-4 col-xl-3 col-md-6 col-10'> */}
            <div className='card s21-card p-4 col-10 text-center'>
                <h3 className='card-title text-center'>Registration</h3>
                <div className='card-body text-center'>
                    {/* <div className="col-lg-6 col-sm-12 d-flex flex-column mt-3"> */}
                    <div className="">
                        <div className="form-floating">
                            <input className="form-control" placeholder="Leave a comment here" id="floatingTextarea" />
                            <label className="text-center" htmlFor="floatingTextarea">
                                Username
                            </label>
                        </div>
                        <div className="form-floating mt-3">
                            <input
                                className="form-control"
                                placeholder="Leave a comment here"
                                id="floatingTextarea" />
                            <label className="text-center" htmlFor="floatingTextarea">
                                Email
                            </label>
                        </div>
                        <div className="form-floating mt-3">
                            <input
                                className="form-control"
                                placeholder="Leave a comment here"
                                id="floatingTextarea" />
                            <label className="text-center" htmlFor="floatingTextarea">
                                Password
                            </label>
                        </div>
                    </div>
                </div>
                <div className='row'>
                    <div className='col text-center'>
                        <button type='button' className='btn s21-btn'>
                            Sign up
                        </button>
                    </div>
                </div>
                <div className='mt-3 text-center'>
                    <h5>Already have an account?</h5>
                    <div className='row mt-3'>
                        <div className='col text-center'>
                            <a href="/auth/login">
                                <button type='button' className='btn s21-subbtn'>
                                    Sigh in
                                </button>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
