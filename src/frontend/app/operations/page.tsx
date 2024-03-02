"use client";

import { useEffect, useState } from 'react';
import FunctionList from './fucntions';
import { apiGetFunctionsAsync } from '@/components/api/FunctionApiHandler';


export default function Operations() {
  const [data, setData] = useState({
    functions: [],
    readable_names: [],
  })

  useEffect(() => {
    apiGetFunctionsAsync().then((data) => setData(data)).catch(e => console.log(e));
  }, [])

  return (
    <FunctionList functions={data.functions} readable={data.readable_names} />
  );
}
