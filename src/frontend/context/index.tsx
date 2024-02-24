"use client";
import { createContext, useState, useContext } from "react";
import { proceedLogin } from "@/components/ApiHandler";

const AppContext = createContext<any>(
    {
        token: "",
        actions: {
            login: async (formData: Object) => { },
            isLoggedIn: () => { },
            logout: () => { }
        }
    }
);

function getTokenFromLocalStorage() {
    if (typeof window === 'undefined') return "";
    return localStorage.getItem('token') || "";
}

export function AppWrapper({ children }: { children: React.ReactNode }) {
    const [store, setStore] = useState({
        token: getTokenFromLocalStorage()
    });

    const actions = {
        login: async (formData: Object) => {
            const data = await proceedLogin(formData);
            const token = data.result.access_token;
            localStorage.setItem('token', token);
            setStore(token);
        },

        isLoggedIn: () => {
            return store.token.length > 0;
        },

        logout: () => {
            localStorage.removeItem('token');
            setStore({
                ...store,
                token: ""
            });
        }
    };

    return (
        <AppContext.Provider value={{ token: store, actions }}>
            {children}
        </AppContext.Provider>
    );
}

export function UseAppContext() {
    return useContext(AppContext);
}