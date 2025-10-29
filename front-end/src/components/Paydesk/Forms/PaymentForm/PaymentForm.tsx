import Cookies from "js-cookie"
import { ChevronRight, CreditCard } from 'lucide-react'
import { useTranslations } from 'next-intl'
import Image from 'next/image'


import { useMutation } from '@tanstack/react-query'
import { AnimatePresence, motion } from 'framer-motion'
import { useEffect, useState } from 'react'
import { PaymentDialog } from './PaymentDialog/PaymentDialog'
import styles from './PaymentForm.module.scss'

type PaymentProps = {
    handleFormStep: (step: 'back' | 'next') => void
}

type Addition = {
    [key: string]: number | null
}

type OrderData = {
    name: string
    phone_number: string
    email: string
    total_amount: number
    items: Record<string, {
        tableName: string
        productId: number
        quantity: number
        weight: number
        additions: Addition
    }>
    delivery_time: string
    delivery_method: string
    location: {
        street: string
        home: string
        homeNumber: string
    }
}
const url = process.env.NEXT_PUBLIC_BACKEND_API_URL
const apiUrl = new URL("order/add_order", url).href
async function orderFetch(orderData: OrderData | null) {
    try {
        const request = new Request(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(orderData)
        })

        const response = await fetch(request)

        if (!response.ok) {
            throw new Error(`Failed to fetch data from ${apiUrl}`)
        }

        const data = await response.json()
        console.log(data)

    } catch (error) {
        console.log(error)
    }
}

export const PaymentForm = ({ handleFormStep }: PaymentProps) => {
    const t = useTranslations("paydesk.thirdForm")

    // const [paymentData, setPaymentData] = useState({})
    const [isDialogOpen, setIsDialogOpen] = useState<boolean>(false)

    const [isOrderAdded, setIsOrderAdded] = useState(false)

    const data = Cookies.get("orderData")

    const orderD: OrderData | null = data ? JSON.parse(data) : null


    const mutation = useMutation({
        mutationFn: orderFetch,
        onSuccess: (data) => {
            console.log(`Data from ${apiUrl}: `, data)
            setIsOrderAdded(true)
        }

    })

    useEffect(() => {
        if (isOrderAdded) {
            const timer = setTimeout(() => {
                setIsOrderAdded(false)
            }, 3000)

            return () => clearTimeout(timer)
        }

    }, [isOrderAdded])

    return (
        <>
            <div className={styles.titleArea}>
                <div className={styles.title}>
                    <span>{t("title")}</span>
                    <Image src={'/icons/under-line.png'} alt={''} width={200} height={10} />
                </div>
            </div>
            <form className={styles.payForm}>
                <fieldset className={styles.choosePayMethod}>
                    <button
                        className={styles.selectedPayMethod}
                        type='button'
                        onClick={() => setIsDialogOpen(true)}
                    >
                        <div className={styles.payIcon}>
                            <CreditCard />
                        </div>
                        <div className={styles.methodInfo}>
                            <div className={styles.methodName}>
                                <span>GooglePay</span>
                            </div>
                            <div className={styles.quota}>
                                <span>Kwota do pobrania: 50 zl</span>
                            </div>
                        </div>
                        <div className={styles.linkIcon}>
                            <ChevronRight />
                        </div>
                    </button>
                </fieldset>
                <div className={styles.submitSegmentBtn}>
                    <button
                        className={styles.prevBtn}
                        type='button'
                        onClick={() => handleFormStep('back')}
                    >
                        Back
                    </button>
                    <button
                        className={styles.nextBtn}
                        type='button'
                        onClick={() => {
                            mutation.mutate(orderD)
                        }}
                    >
                        Pay
                    </button>
                </div>
            </form >
            <AnimatePresence>
                {isOrderAdded && (
                    <motion.div
                        className={styles.notificationWindow}
                        initial={{ opacity: 0, y: 100, x: 10, rotate: -10 }}
                        animate={{ opacity: 1, y: "-50%", x: "-50%", rotate: 0 }}
                        exit={{ opacity: 0, y: 100, x: 10, rotate: -10 }}
                        transition={{ type: "spring", stiffness: 100, damping: 10 }}
                        style={{ top: "50%", left: "50%", position: "fixed", zIndex: 1000 }}
                    >
                        <div className={styles.notificationContainer}>
                            <span className={styles.notificationText}>
                                The order is added✅
                            </span>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
            <PaymentDialog isDialogOpen={isDialogOpen} setIsDialogOpen={setIsDialogOpen} />
        </>
    )
} 