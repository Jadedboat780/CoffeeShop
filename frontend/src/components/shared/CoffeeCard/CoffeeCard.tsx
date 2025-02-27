import {FC} from "react";
import {CoffeeItem} from "@/types/coffee.ts";
import styles from './CoffeeCard.module.css'


export const CoffeeCard: FC<CoffeeItem> = ({name, description, price, type, image}) => {
    return <div className={styles.card}>
        <img src={image} alt=""/>
        <div className={styles.container}>
            <div style={{display: 'flex', flexDirection: 'row'}}>
                <h3 className={styles.title}>{name}</h3>
                <span className={styles.category}>{type}</span>
            </div>
            <p className={styles.description}>{description}</p>
            <button>{price} ₽</button>
        </div>
    </div>
}