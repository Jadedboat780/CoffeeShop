import { setSearchText } from "@/store/searchStore.ts";
import type { CoffeeItem } from "@/types/coffee.ts";
import type { FC } from "react";
import styles from "./CoffeeCard.module.css";

export const CoffeeCard: FC<CoffeeItem> = ({ name, description, price, type, image }) => {
	return (
		<div className={styles.card}>
			<img src={image} alt="" />
			<div className={styles.container}>
				<div style={{ display: "flex", flexDirection: "row" }}>
					<h3 className={styles.title}>{name}</h3>
					<button className={styles.category} type="button" onClick={() => setSearchText(type.toLowerCase())}>
						{type}
					</button>
				</div>
				<p className={styles.description}>{description}</p>
				<button type="button" onClick={() => console.log("a")}>
					{price} ₽
				</button>
			</div>
		</div>
	);
};
