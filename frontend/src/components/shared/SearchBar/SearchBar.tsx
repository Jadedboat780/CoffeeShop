import styles from './SearchBar.module.css'
import {useState} from "react";

export const SearchBar = () => {
    const [searchInput, setSearchInput] = useState("");

    return <div className={styles.search_bar}>
        <input type="text"
               value={searchInput}
               onChange={(e) => setSearchInput(e.target.value)}
               placeholder="What are you looking for?"/>
    </div>
}