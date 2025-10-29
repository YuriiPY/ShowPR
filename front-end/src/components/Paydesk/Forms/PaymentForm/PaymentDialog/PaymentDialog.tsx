import { Plus, X } from 'lucide-react'



import ApplePayIcon from '@/components/svgIcons/ApplePayIcon'
import CashIcon from '@/components/svgIcons/CashIcon'
import GooglePayIcon from '@/components/svgIcons/GooglePayIcon'
import { motion, useAnimation } from 'framer-motion'
import { useEffect, useRef } from 'react'
import styles from './PaymentForm.module.scss'


type PaymentFormProps = {
    isDialogOpen: boolean,
    setIsDialogOpen: (status: boolean) => void
}


export const PaymentDialog = ({ isDialogOpen, setIsDialogOpen }: PaymentFormProps) => {

    const dialogRef = useRef<HTMLDialogElement>(null)

    const appearAnimation = useAnimation()

    // const handlePopUp = useCallback(async () => {
    //     const dialog = dialogRef.current
    //     if (!dialog) return

    //     if (isDialogOpen) {
    //         if (!dialog.open) {
    //             dialog.showModal()
    //             document.body.style.overflow = 'hidden'
    //             appearAnimation.set({ y: 100, opacity: 0 })
    //             appearAnimation.start({ y: 0, opacity: 1, transition: { duration: .3 } })
    //         }

    //     } else {
    //         if (dialog.open) {
    //             await appearAnimation.start({
    //                 y: 100,
    //                 opacity: 0,
    //                 transition: { duration: 0.3, ease: "easeInOut" }
    //             })
    //             dialog.close()
    //             document.body.style.overflow = ''
    //         }
    //     }
    // }, [appearAnimation, isDialogOpen])



    useEffect(() => {
        // handlePopUp()



        const dialog = dialogRef.current
        if (!dialog) return

        const handlePopUp = async () => {
            if (isDialogOpen) {
                if (!dialog.open) {
                    dialog.showModal()
                    document.body.style.overflow = 'hidden'
                    appearAnimation.set({ y: 100, opacity: 0 })
                    appearAnimation.start({ y: 0, opacity: 1, transition: { duration: .3 } })
                }

            } else {
                if (dialog.open) {
                    await appearAnimation.start({
                        y: 100,
                        opacity: 0,
                        transition: { duration: 0.3, ease: "easeInOut" }
                    })
                    dialog.close()
                    document.body.style.overflow = ''
                }
            }
        }

        handlePopUp()

        const handleCancel = (e: Event) => {
            e.preventDefault()
            setIsDialogOpen(false)
        }


        dialog.addEventListener('cancel', handleCancel)

        return () => dialog.removeEventListener('cancel', handleCancel)
    }, [appearAnimation, isDialogOpen, setIsDialogOpen])

    return (
        <dialog
            className={styles.selectMethodPopUp}
            ref={dialogRef}
            onClick={(e: React.MouseEvent<HTMLDialogElement>) => {
                if (e.target === e.currentTarget) setIsDialogOpen(false)
            }}
        >
            <motion.div
                className={styles.selectPopUpContainer}
                animate={appearAnimation}
            >
                <aside>
                    <div className={styles.popUpHeader}>
                        <button
                            className={styles.closePopUpBtn}
                            onClick={() => {
                                setIsDialogOpen(false)
                            }}
                        >
                            <X className={styles.closeBtnIcon} />
                        </button>
                    </div>
                    <div className={styles.Content}>
                        <div className={styles.paymentMethodContent}>
                            <div className={styles.title}>
                                <h2>Method payment</h2>
                            </div>
                            <div className={styles.paymentMethodGroup}>
                                <div className={styles.addCardInfo}>
                                    <h3>Credit and debit cards</h3>
                                    <button className={styles.addCardButton}>
                                        <span>
                                            <Plus />
                                        </span>
                                        Add new card
                                    </button>
                                </div>
                            </div>
                            <div className={styles.paymentMethodGroup}>
                                <div className={styles.paymentMethodList}>
                                    <h3>Other payment methods</h3>
                                    <button
                                        className={styles.paymentMethodItem}
                                    >
                                        <span><ApplePayIcon /></span>
                                        <span className={styles.methodName}>Apple Pay</span>
                                        <div className={styles.buttonImitation}>
                                            <span>Select</span>
                                        </div>
                                    </button>
                                    <button className={styles.paymentMethodItem}>
                                        <span><GooglePayIcon /></span>
                                        <span className={styles.methodName}>Google Pay</span>
                                        <div className={styles.buttonImitation}>
                                            <span>Select</span>
                                        </div>
                                    </button>
                                    <button className={styles.paymentMethodItem}>
                                        <span><CashIcon /></span>
                                        <span className={styles.methodName}>Cash</span>
                                        <div className={styles.buttonImitation}>
                                            <span>Select</span>
                                        </div>
                                    </button>
                                </div>
                            </div>

                        </div>
                    </div >
                </aside >
            </motion.div >
        </dialog >
    )
}