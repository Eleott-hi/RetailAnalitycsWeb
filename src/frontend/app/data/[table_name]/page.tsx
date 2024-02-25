"use client";

import { useEffect, useState } from "react";
import ItemList from "./ItemList"
import { apiGetTableAsync, apiGetTableFieldsAsync } from "@/components/ApiHandler";

export default function TablePage({ params }: { params: { table_name: string } }) {
    const [data, setData] = useState<any>(null);

    useEffect(() => {
        apiGetTableAsync(params.table_name).then(
            ([table, fields]) => {
                console.log("TablePage", table, fields);
                setData({
                    table: table,
                    fields: fields,
                })
            }
        );
    }, []);


    return (
        data &&
        <ItemList t_name={params.table_name} columns={data.fields} items={data.table} />
    );
}
