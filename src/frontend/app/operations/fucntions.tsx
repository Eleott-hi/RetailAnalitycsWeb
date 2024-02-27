"use client";
import { useState, useEffect } from 'react';
import Table from "@/components/Table";
import TableItemHandler from "@/components/TableItemHandler"
import { ExportCSV } from '@/components/ImportExport';
import { apiGetFunctionInfoAsync, apiExecuteFunctionAsync } from '@/components/api/FunctionApiHandler';

import ErrorDialog from '@/components/ErrorDialog';

export default function FunctionList({ functions, readable }: { functions: string[], readable: string[] }) {
    const [table, setTable] = useState<any[] | null>(null);
    const [isItemDialog, setIsItemDialog] = useState(false);
    const [itemDialog, setItemDialog] = useState({
        header: "",
        content: {},
        handleClose: (is_confirmed: boolean) => { }
    });
    const [isErrorDialog, setIsErrorDialog] = useState(false);
    const [errorProps, setErrorProps] = useState({
        header: "Invalid function parameters",
        content: "Please check your input and try again",
        handleClose: () => { setIsErrorDialog(false) }
    });

    const ExecuteFunction = (f_name: string, params: any, on_done: (data: any[]) => void) => { setTable([]); apiExecuteFunctionAsync(f_name, params).then(on_done).catch(error => { console.error(error); setTable(null); setIsErrorDialog(true); }); }

    const OpenParametersDialog = (f_name: string, data: any) => {
        setItemDialog({
            header: "Enter parameters of " + f_name + ":",
            content: data,
            handleClose: (is_confirmed: boolean, params: any = null) => {
                if (is_confirmed) {
                    console.log("CONFIRMED", params);
                    ExecuteFunction(f_name, params, (data: any[]) => { setTable(data); setIsItemDialog(false) });
                } else {
                    console.log("CANCELED");
                    setIsItemDialog(false)
                }
            }
        })
        setIsItemDialog(true);
    }

    const ParametersDialogLogic = (f_name: string, data: any) => {
        if (Object.keys(data).length === 0) {
            ExecuteFunction(f_name, {}, setTable);
        } else {
            OpenParametersDialog(f_name, data);
        }
    }

    const FunctionHandler = (f_name: string) => apiGetFunctionInfoAsync(f_name).then((data) => ParametersDialogLogic(f_name, data)).catch(error => console.error(error));

    return (
        <div className="p-4 row">
            <div className="col-12 text-center">
                <h1>Operations</h1>
            </div>
            <div className="col-lg-6 col-sm-12 d-flex flex-column mt-3">
                <ol>
                    {
                        functions.map((f_name, index) => (
                            <li className='mt-1' key={f_name}>
                                <button type="button" className='btn s21-btn' onClick={() => FunctionHandler(f_name)}>
                                    {readable[index]}
                                </button>
                            </li>
                        ))
                    }
                </ol>
            </div>
            {
                table && (
                    <div className="col-lg-6 col-sm-12 d-flex flex-column mt-3">
                        <div className="card s21-card">
                            <Table data={table}></Table>
                        </div>
                        <button type="button" className="btn s21-btn mt-2 ms-auto" onClick={() => ExportCSV(table)}>
                            Export
                        </button>
                    </div>
                )
            }
            {isItemDialog && (<TableItemHandler props={itemDialog} />)}
            {isErrorDialog && (<ErrorDialog props={errorProps} />)}
        </div>
    );
}
