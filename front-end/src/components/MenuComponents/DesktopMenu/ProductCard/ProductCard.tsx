'use client'

import Image from 'next/image'
import { forwardRef, useState } from 'react'

import clsx from 'clsx'
import { useTranslations } from 'next-intl'
import ProductPopUp from '../ProductPopUp/ProductPopUp'
import styles from "./ProductCard.module.scss"

interface ProductCard {
    index: number
    itemId: number
    tableName: string
    name: string
    img: string
    description: string
    price: number
    type: "by weight" | "by portion"
    status: boolean
    menuTabsRef: React.MutableRefObject<{ [key: string]: HTMLButtonElement | null }>
}

const ProductCard = forwardRef<HTMLButtonElement, ProductCard>(
    ({ index, tableName, itemId, name, img, description, price, type, status, menuTabsRef }, ref) => {

        const [isPopUpOpen, setIsPopUpOpen] = useState(false)

        const t = useTranslations("TextForScreenReader.menuText")

        return (
            <>
                <button
                    ref={index === 0 ? ref : null}
                    type='button'
                    aria-label={tableName + " " + t("menuButton")}
                    // disabled={!status}
                    // className={clsx(styles.productCard, { [styles.disabled]: !status })}
                    className={styles.productCard}
                    onKeyDown={(e) => {
                        if (index % 2 === 0) {
                            if (e.key === "ArrowLeft") {
                                menuTabsRef.current[tableName]?.focus()
                            }
                        }
                    }}
                    onClick={() => { setIsPopUpOpen(true) }}>
                    <div className={styles.singleDelicious} data-type="dumplings">
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


                <ProductPopUp product={{
                    tableName: tableName,
                    itemId: itemId,
                    name: name,
                    img: img,
                    description: description,
                    price: price,
                    status: status,
                    type: type
                }}
                    closePopUp={() => setIsPopUpOpen(false)}
                    isPopUpOpen={isPopUpOpen}
                />

            </>
        )
    }
)

ProductCard.displayName = 'ProductCard'

export default ProductCard