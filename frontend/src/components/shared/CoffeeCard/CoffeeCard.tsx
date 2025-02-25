import styles from './CoffeeCard.module.css'
import {CoffeeItem} from "@/types/coffee";


export const CoffeeCard = ({title, description, price, image_url}: CoffeeItem) => {
    return <div className={styles.card}>
        <img className={styles.img} src={image_url} alt=""/>
        <div className={styles.container}>
            <h3 className={styles.title}>{title}</h3>
            <p className={styles.description}>{description}</p>
            <button><p>{price} ₽</p></button>
        </div>
    </div>
}