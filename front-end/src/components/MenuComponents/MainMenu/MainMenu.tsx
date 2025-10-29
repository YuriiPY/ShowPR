'use client'

import BasketPopUp from '../BasketPopUp/BasketPopUp'
import Menu from '../Menu/Menu'
import styles from "./MainMenu.module.scss"


export default function MainMenu() {



    return (
        <section className={styles.deliciousArea}>
            <Menu />
            <BasketPopUp />
        </section>
    )
}