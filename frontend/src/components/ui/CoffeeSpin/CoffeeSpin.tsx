import CoffeeImg from "@/assets/coffee.png";
import styles from "./CoffeeSpin.module.css";

export const CoffeeSpin = () => {
	return (
		<div className={styles.container}>
			<img src={CoffeeImg} alt="biryani img" className={styles.coffee_img} />
		</div>
	);
};
