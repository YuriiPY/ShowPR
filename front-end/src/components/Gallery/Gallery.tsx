'use client'

import Image from 'next/image'

import { AnimatePresence, motion } from 'framer-motion'
import { CircleX } from 'lucide-react'
import { useTranslations } from 'next-intl'
import { useEffect, useRef, useState } from 'react'
import styles from './Gallery.module.scss'


export default function Gallery() {

    const t = useTranslations("TextForScreenReader")

    const [dialogData, setDialogData] = useState({
        isDialogOpen: false,
        imgUrl: ""
    })
    const dialogRef = useRef<HTMLDialogElement | null>(null)


    useEffect(() => {
        const dialogEl = dialogRef.current

        if (!dialogEl) return

        if (dialogData.isDialogOpen) {
            document.body.style.overflow = 'hidden'
            dialogEl.showModal()
        } else {
            document.body.style.overflow = ''
        }

        const closeDialog = (e: Event) => {
            e.preventDefault()
            setDialogData({
                isDialogOpen: false,
                imgUrl: ''
            })
        }

        dialogEl.addEventListener('cancel', closeDialog)

        return () => {
            dialogEl.removeEventListener('cancel', closeDialog)
        }
    }, [dialogData])

    const photoGalleryList = [
        "/Gallery/cake.png",
        "/Gallery/cheese.png",
        "/Gallery/cherry-dumplings.png",
        "/Gallery/chops.png",
        "/Gallery/napoleon.png",
        "/Gallery/roll.png",
    ]

    return (
        <>
            <AnimatePresence>
                {dialogData.isDialogOpen &&
                    <dialog
                        ref={dialogRef}
                        onClick={(e: React.MouseEvent<HTMLDialogElement>) => {
                            if (e.target === e.currentTarget) {
                                setDialogData({
                                    isDialogOpen: false,
                                    imgUrl: ''
                                })
                            }
                        }}
                        className={styles.mainDialog}
                    >
                        <motion.div
                            className={styles.imgDialogContainer}
                            initial={{ opacity: 0, y: 100 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: 100 }}
                            transition={{ duration: .3, ease: "easeInOut" }}
                            onAnimationComplete={(definition) => {
                                if (definition === "exit") { dialogRef.current?.close() }
                            }}
                        >
                            <button
                                type='button'
                                aria-label={t("buttons.closePopUpButton")}
                                className={styles.dialogCloseBtn}
                                onClick={() => setDialogData({
                                    isDialogOpen: false,
                                    imgUrl: ''
                                })}>
                                <CircleX />
                            </button>
                            <Image src={dialogData.imgUrl} alt={''} width={500} height={500} />
                        </motion.div>
                    </dialog>
                }
            </AnimatePresence>
            <section className={styles.GalleryArea}>
                <div aria-hidden={true} className={styles.Icon1}>
                    <Image src="/icons/AboutAreaIcons/1.png" alt="icon1" width={150} height={200} />
                </div>
                <div aria-hidden={true} className={styles.Icon2}>
                    <Image src="/icons/AboutAreaIcons/2.png" alt="icon2" width={150} height={150} />
                </div>
                <div aria-hidden={true} className={styles.Icon3}>
                    <Image src="/icons/AboutAreaIcons/3.png" alt="icon3" width={150} height={130} />
                </div>
                <div className={styles.Container}>
                    <div className={styles.Row}>
                        <h3>Photo Gallery</h3>
                    </div>
                </div>
                <div className={styles.Container}>
                    <div className={styles.ImgContainer}>
                        {photoGalleryList.map((url, index) => (
                            <button
                                type='button'
                                aria-label={t("galleryText.buttonText")}
                                key={index}
                                onClick={() => {
                                    setDialogData({
                                        isDialogOpen: true, imgUrl: url
                                    })
                                }}>
                                <div className={styles.Img}>
                                    <Image src={url} alt={''} width={500} height={400} />
                                </div>
                            </button>
                        ))}
                    </div>
                </div>

            </section >
        </>
    )
}