"use client";


import Script from "next/script";
import { usePathname } from 'next/navigation';
import Image from "next/image";
import { UseAppContext } from "@/context";


const navLinksUnauthorised = [
    { href: "/auth/login", name: "Log in" },
    { href: "/auth/registration", name: "Sign up" },
]
const navLinksAuthorised = [
    { href: "/data", name: "Data" },
    { href: "/operations", name: "Operations" },
    { href: "/logout", name: "Log out" },
];

export default function Header() {
    const pathname = usePathname();
    const { actions } = UseAppContext();


    return (
        <header>
            <Script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
                integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
                crossOrigin="anonymous"
            />

            <nav className="navbar navbar-expand-md navbar-dark fixed-top p-0"
                style={{
                    backgroundColor: "var(--dark-background-color)",
                    minHeight: "150px"
                }}>
                <div className="container-fluid">
                    <a className="" href="/">
                        <Image className='' src="/main.png" alt="Logo" width={150} height={150} />
                    </a>

                    <div className='text-center'
                        style={{
                            minWidth: "200px"
                        }}>
                        <a className="navbar-brand" href="/">
                            RetailAnalitycs v2.0 Web
                        </a>
                    </div>

                    <button className="navbar-toggler"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#navbarCollapse"
                        aria-controls="navbarCollapse"
                        aria-expanded="false"
                        aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    <div className="collapse navbar-collapse" id="navbarCollapse">
                        <ul className="navbar-nav ms-auto mb-2 mb-md-0">
                            {
                                (actions.isLoggedIn() ? navLinksAuthorised : navLinksUnauthorised).map(
                                    (link) => {
                                        const isActive = pathname.startsWith(link.href);

                                        if (link.name === "Log out")
                                            return (
                                                <li key={link.name} className="nav-item">
                                                    <a href={"/auth/login"}
                                                        onClick={() => actions.logout()}
                                                        className={"nav-link " + (isActive ? "active s21-active-link" : "")}
                                                        aria-current="page">
                                                        {link.name}
                                                    </a>
                                                </li>
                                            )

                                        return (
                                            <li key={link.name} className="nav-item">
                                                <a href={link.href}
                                                    className={"nav-link " + (isActive ? "active s21-active-link" : "")}
                                                    aria-current="page">
                                                    {link.name}
                                                </a>
                                            </li>
                                        )
                                    }
                                )
                            }
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
    );
}
