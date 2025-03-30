import { useSearchStore } from "@/store";
import styles from "./SearchBar.module.css";

export const SearchBar = () => {
	const { text, setText } = useSearchStore();

	return (
		<div className={styles.search_bar}>
			<input type="search" value={text} placeholder="Search for coffee..." onChange={(e) => setText(e.target.value)} />
		</div>
	);
};
