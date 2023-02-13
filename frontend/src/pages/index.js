import Head from 'next/head'
import Image from 'next/image'
import { Inter } from '@next/font/google'
import styles from '@/styles/Home.module.css'
import Link from 'next/link'

export default function Home() {
  return (
    <>
      <div>
        <h1>Welcome to Finance Portfolio Generator</h1>
        <Link href='/searchInvestment'>
          <button>Search For Investments</button>
        </Link>
        <Link href='/generatePortfolio'>
          <button>Generate a Portfolio</button>
        </Link>
      </div>
    </>
  )
}
