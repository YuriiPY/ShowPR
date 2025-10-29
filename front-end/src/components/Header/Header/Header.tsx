'use client'

import { Plus } from 'lucide-react'
import { useTranslations } from 'next-intl'
import Image from 'next/image'
import Link from 'next/link'
import { useEffect, useMemo, useRef, useState } from 'react'
import { useInView } from 'react-intersection-observer'


import clsx from 'clsx'
import { AnimatePresence, motion, useScroll } from 'framer-motion'
import { usePathname } from 'next/navigation'
import BreakupSection from '../../breakups/BreakupSection'
import Button from '../../buttons/Button/Button'
import SegmentedButton from '../../buttons/SegmentedButton/SegmentedButton'
import { LanguageSelector } from '../../LanguageSelector/LanguageSelector'
import ActiveHeader from '../ActiveHeader/ActiveHeader'
import style from './Header.module.scss'


interface HeaderTypes {
    dataImg: { url: string }[] | string
    isActiveHeader: "on" | "off"
    isButton: "on" | "off"
}


export default function Header({ dataImg, isActiveHeader, isButton }: HeaderTypes) {

    const t = useTranslations("NavigateButtons")
    const ButtonsName = useTranslations("MainPage.ButtonsName")
    const screenReaderTranslationText = useTranslations("TextForScreenReader")

    const firstPathName = usePathname()

    const pathName = firstPathName.slice(3) === ""
        ? "/"
        : firstPathName.slice(3)

    const NavigationButtonData = useMemo(() => ([
        {
            buttonName: t("home"),
            link: "/",
            isSelected: pathName === '/'
        },
        {
            buttonName: t("menu"),
            link: "/menu",
            isSelected: pathName === '/menu'
        },
        {
            buttonName: t("contacts"),
            link: "/contacts",
            isSelected: pathName === '/contacts'
        }
    ]), [t, pathName])

    const [currentButtonOpacity, setCurrentButtonOpacity] = useState(1)


    const { ref, inView } = useInView()

    const backgroundDivRef = useRef<HTMLDivElement>(null)
    const sectionRef = useRef<HTMLElement>(null)

    const isArrayDataImg = Array.isArray(dataImg)

    // const backgroundImgUrl = isArrayDataImg ? dataImg[currentPhotoIndex].url : dataImg

    const currentPhotoIndexRef = useRef(0)

    const [isImagesLoading, setIsImagesLoading] = useState(true)

    const { scrollYProgress } = useScroll({
        target: sectionRef,
        offset: ["end start", "start start"]
    })

    useEffect(() => {
        scrollYProgress.on("change", (e) => {
            if (e >= 0.7) {
                setCurrentButtonOpacity(e)
            }
        })
    }, [scrollYProgress])

    useEffect(() => {
        if (Array.isArray(dataImg)) {
            const preloadImages = async () => {
                await Promise.all(
                    dataImg.map((item) => {
                        return new Promise((resolve) => {
                            const img = new window.Image()
                            img.src = item.url
                            img.onload = resolve
                            img.onerror = resolve

                        })
                    })
                )
                setIsImagesLoading(false)
            }

            preloadImages()
        }
    }, [dataImg])


    useEffect(() => {
        if (isImagesLoading) return
        if (Array.isArray(dataImg)) {
            let intervalOfBackImg: NodeJS.Timeout | null = null
            if (isArrayDataImg && inView) {
                intervalOfBackImg = setInterval(() => {
                    currentPhotoIndexRef.current = (currentPhotoIndexRef.current + 1) % dataImg.length
                    const nextUrl = dataImg[currentPhotoIndexRef.current].url
                    if (backgroundDivRef.current) {
                        backgroundDivRef.current.style.backgroundImage = `url(${nextUrl})`
                    }
                }, 5000)
                return () => {
                    if (intervalOfBackImg) clearInterval(intervalOfBackImg)
                }
            }
        } else {
            if (backgroundDivRef.current) {
                backgroundDivRef.current.style.backgroundImage = `url(${dataImg})`
            }
        }
    }, [dataImg, isArrayDataImg, inView, isImagesLoading])

    // const previousScrollY = useRef(0)

    // const handleScroll = useCallback(() => {
    //     requestAnimationFrame(() => {
    //         const currentScrollY = window.scrollY

    //         setCurrentButtonOpacity((prev) => {
    //             if (currentScrollY > previousScrollY.current) {
    //                 return Math.max((prev - 0.15), 0)
    //             } else if (currentScrollY < previousScrollY.current) {
    //                 return Math.min((prev + 0.2), 1)
    //             }
    //             return prev
    //         }
    //         )

    //         previousScrollY.current = currentScrollY
    //     })
    // }, [])

    //SCROLL -> OPACITY
    // useEffect(() => {
    //     if (inView) {
    //         window.addEventListener('scroll', handleScroll)
    //     }

    //     return () => {
    //         window.removeEventListener('scroll', handleScroll)
    //     }
    // }, [handleScroll, inView])


    return (
        <section ref={sectionRef} className={style.header}>
            <AnimatePresence>
                {(isActiveHeader === "on" && !inView)
                    && <ActiveHeader />}
            </AnimatePresence>
            <div className={style.backgroundOverlay}></div>
            <div ref={backgroundDivRef} className={style.backgroundOverlayImg}></div>

            <div className={style.topHeaderContainer}>
                <div className={style.primaryHeader}>
                    <div className={style.socialBtn}>
                        <nav aria-label={screenReaderTranslationText("socialLink.navText")} className={style.socialNav}>
                            <ul>
                                <li id="first-social-link">
                                    <Link aria-label={screenReaderTranslationText("socialLink.facebook")} href="https://www.facebook.com/alina.pierogowa">
                                        <Image className={style.socialIcon} src="/social-media/facebook.png" alt="Facebook" width="25" height="25" />
                                    </Link>
                                </li>
                                <li id="second-social-link">
                                    <Link aria-label={screenReaderTranslationText("socialLink.instagram")} href="https://www.instagram.com/alina_pierogowa">
                                        <Image className={style.socialIcon} src="/social-media/instagram.png" alt="Instagram" width="25" height="25" />
                                    </Link>
                                </li>
                            </ul>
                        </nav>
                    </div>
                    <div className={style.headerImg}>
                        <div className={style.headerImgContainer}>
                            <Link href="/"
                                aria-label="Go to homepage"
                            >
                                <Image src="/favicon/favicon.jpg" alt="favicon" width="100" height="100" />
                            </Link>
                        </div>
                    </div>
                    <div className={style.lang}>
                        <div className={style.languageSelectorContainer}>
                            <LanguageSelector />
                        </div>
                    </div>
                </div>
                <div className={style.gradientLine}></div>

                <div ref={ref} className={style.headerNavigationBtn}>
                    <div className={style.btnContainer}>
                        <nav className={style.linkHeader}>
                            <SegmentedButton type={'text'} hoverType={'underline'} buttonsList={NavigationButtonData} selectType={'hoverStyle'} selfSelect={false} />
                        </nav>
                    </div>
                </div>
                <div className={style.underHeader}>
                    <div className={style.elementBackground}>
                        <Image src="/Header/Big_Logo.png"
                            alt='Alina Pierogowa Jedzenie z Wroclawia'
                            layout="intrinsic"
                            width={500}
                            height={300} />
                    </div>
                    {
                        isButton === "on" && <>
                            <motion.div
                                animate={{
                                    opacity: currentButtonOpacity, scale: currentButtonOpacity
                                }}
                                transition={{ duration: .3 }}
                            >
                                <Button type='elevated' buttonName={ButtonsName("order")} buttonHover='changeColor' link='/menu' icon={Plus} />
                            </motion.div>
                            <div className={clsx(style.slideBtnContainer, { [style.visible]: !inView })}>
                                <Button type="elevated" buttonName={ButtonsName("order")} link='/menu' icon={Plus} buttonHover='changeColor' />
                            </div>
                        </>
                    }
                </div>
            </div>
            <BreakupSection type='up' />
        </section >
    )
}
