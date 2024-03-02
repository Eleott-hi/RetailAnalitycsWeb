"use client";

import { createContext, useState, useContext } from "react";
import { apiLoginAsync, apiRegisterAsync, apiIsLoggedIn } from "@/components/api/AuthenticationApiHandler";
import { getTokenFromLocalStorage, setTokenToLocalStorage, removeTokenFromLocalStorage } from "@/components/api/Common";

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



export function AppWrapper({ children }: { children: React.ReactNode }) {
    const [store, setStore] = useState({
        token: getTokenFromLocalStorage()
    });

    const actions = {
        register: async (formData: Object) => {
            const data = await apiRegisterAsync(formData);
            return data;
        },

        login: async (formData: Object) => {
            const data = await apiLoginAsync(formData);
            const token = data.result.access_token;
            setTokenToLocalStorage(token);
            setStore({ ...store, token: token });
        },

        isLoggedIn: () => {
            const res = getTokenFromLocalStorage();
            return res && res !== '';
        },

        logout: () => {
            removeTokenFromLocalStorage();
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
