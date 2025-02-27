import styles from './SearchBar.module.css'
import {useSearchStore} from "@/store";

export const SearchBar = () => {
    const {text, setText} = useSearchStore();

    return <div className={styles.search_bar} role="search">
        <input type="text"
               value={text}
               placeholder="Search for coffee..."
               onChange={(e) => setText(e.target.value)}
        />
    </div>
}