import Link from 'next/link'
import Head from 'next/head'
// import 'bootstrap/dist/css/bootsrap.min.css'
// import styles from '@/styles/Home.module.css'

export default function Home() {
  return (
    <>
      <Head>
        <title>Investor Aid</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet"></link>
      </Head>
      <h1>Stock Watchlist</h1>
      {/* <div className={styles.container}>
        <h1 className={styles.title}>Stock Watchlist</h1>
      </div> */}
    </>
  )
}
