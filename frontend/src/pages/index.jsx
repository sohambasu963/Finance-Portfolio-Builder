import Link from "next/link"
import Head from "next/head"
import { useState, useEffect } from "react"
import StockSearch from "@/components/StockSearch"
// import 'bootstrap/dist/css/bootsrap.min.css'
// import styles from '@/styles/Home.module.css'

export default function Home() {

  const [search, setSearch] = useState('')

  function handleSearch(e) {
    e.preventDefault();
    setSearch(e.target.value);
  }

  useEffect(() => {
    console.log(search)
  }, [search])

  return (
    <>
      <Head>
        <title>Investor Aid</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet"></link>
      </Head>
      <div className="header">
        <h1>Stock Watchlist</h1>
        <p>Search for stocks below to add them to your watchlist</p>
      </div>
      <div className="container">
        <StockSearch />
      </div>
    </>
  )
}
