import React from "react"
import styles from "./StockSearch.module.css"
import SearchIcon from '@mui/icons-material/Search';

export default function StockSearch({ data }) {
  return (
    <div className={styles.StockSearch}>
      <div className={styles.stockSearchInput}>
        <input 
          type="text"
          placeholder="Search for a stock..."
        />
        <div className={styles.searchIcon}>
          <SearchIcon />
        </div>
      </div>
    </div>
  )
}