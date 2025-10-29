'use client'

import clsx from 'clsx'
import Image from 'next/image'
import { useState } from 'react'

import MobileProductPopUp from '../MobileProductPopUp/MobileProductPopUp'
import styles from "./MobileProductCard.module.scss"

type MobileProductCard = {
    itemId: number
    tableName: string
    name: string
    img: string
    description: string
    price: number
    type: "by weight" | "by portion"
    status: boolean

}

export default function MobileProductCard({ tableName, itemId, name, img, description, price, type, status }: MobileProductCard) {

    const [isPopUpOpen, setIsPopUpOpen] = useState(false)

    return (
        <>
            <button
                // className={clsx(styles.productCard, { [styles.disabled]: !status })}
                className={styles.productCard}
                onClick={() => { setIsPopUpOpen(true) }}>
                <div className={styles.singleDelicious}>
                    <div className={styles.thumb}>
                        <Image src={img} alt="product card" height="166" width="166" />
                    </div>
                    <div className={styles.productInform}>
                        <div className={styles.informationContainer}>
                            <h3>{name}</h3>
                            <p>{description}</p>
                        </div>
                        <span className={clsx(styles.productPrice, type === "by portion" ? styles.byPortionPrice : styles.byWeightPrice)}>
                            {price}
                        </span>
                    </div>
                </div>
            </button >
            {
                isPopUpOpen && <MobileProductPopUp product={{
                    tableName: tableName,
                    itemId: itemId,
                    name: name,
                    img: img,
                    description: description,
                    price: price,
                    status: status,
                    type: type
                }} closePopUp={() => setIsPopUpOpen(false)} />
            }
        </>
    )
}