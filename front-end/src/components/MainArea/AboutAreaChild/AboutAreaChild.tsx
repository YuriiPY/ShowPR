'use client'

import { BadgePlus } from 'lucide-react'
import Image from 'next/image'
import { useInView } from 'react-intersection-observer'

import clsx from 'clsx'
import { useTranslations } from 'next-intl'
import Button from '../../buttons/Button/Button'
import styles from './AboutAreaChild.module.scss'

interface chAboutComponentProperties {
    id: number,
    title: string,
    description: string,
    imgBig: string,
    imgSmall: string,
    link: string
}

export default function AboutChildComponent({ id, title, description, imgBig, imgSmall, link }: chAboutComponentProperties) {

    const ButtonsName = useTranslations("MainPage.ButtonsName")

    const { ref, inView } = useInView({
        triggerOnce: true,
        threshold: 0.2
    })

    return (
        <div ref={ref} key={id} className={(id + 1) % 2 === 0 ? styles.childAreaMiddleContainer : styles.childAreaContainer}>
            <div className={clsx(styles.colLg6, styles.left, { [styles.visible]: inView })}>
                <div className={styles.aboutInfoWrap}>
                    <h1>{title}</h1>
                    <span className={styles.smallDash}></span>
                    <p>{description}</p>
                </div>
            </div>
            <div className={clsx(styles.colLg6, styles.right, { [styles.visible]: inView })}>
                <div className={styles.aboutImgWrap}>
                    <div className={styles.imgAbout}>
                        <div className={styles.img1}>
                            <Image src={imgBig} alt="" width={350} height={350} />
                        </div>
                        <div className={styles.img2}>
                            <Image src={imgSmall} alt="" width={150} height={150} />
                        </div>
                    </div>
                    <div className={styles.aboutMenuBtnContainer}>
                        <Button type="elevated" buttonName={ButtonsName("makeOrder")} icon={BadgePlus} buttonHover="changeColor" link={link} />
                    </div>
                </div>
            </div>
        </div>
    )
}