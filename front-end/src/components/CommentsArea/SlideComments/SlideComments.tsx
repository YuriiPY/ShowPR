'use client'


import { ArrowBigLeft, ArrowBigRight } from 'lucide-react'
import { useTranslations } from 'next-intl'
import { useEffect, useState } from 'react'
import Slider, { CustomArrowProps } from "react-slick"
import "slick-carousel/slick/slick-theme.css"
import "slick-carousel/slick/slick.css"

import BreakupSection from '../../breakups/BreakupSection'
import Comment from '../Comment/Comment'
import styles from './SlideComments.module.scss'

const commentInformation = [
    {
        comment: "It was sooo delicious! I enjoyed my meal so much(vareniki with smetana&cabbage), I want to eat here everyday 🤤💔",
        authorName: "Svitlana Voznyuk",
        authorImg: "/MainPage/Testimonial/avatars/unnamed.png",
        countStars: 5
    },
    {
        comment: "It was sooo delicious! I enjoyed my meal so much(vareniki with smetana&cabbage), I want to eat here everyday 🤤💔",
        authorName: "Svitlana Voznyuk",
        authorImg: "/MainPage/Testimonial/avatars/unnamed.png",
        countStars: 5
    },
    {
        comment: "It was sooo delicious! I enjoyed my meal so much(vareniki with smetana&cabbage), I want to eat here everyday 🤤💔",
        authorName: "Svitlana Voznyuk",
        authorImg: "/MainPage/Testimonial/avatars/unnamed.png",
        countStars: 5
    },
    {
        comment: "It was sooo delicious! I enjoyed my meal so much(vareniki with smetana&cabbage), I want to eat here everyday 🤤💔",
        authorName: "Svitlana Voznyuk",
        authorImg: "/MainPage/Testimonial/avatars/unnamed.png",
        countStars: 5
    }
]

// interface ArrowProps {
//     className?: string
//     style?: React.CSSProperties
//     onClick?: React.MouseEventHandler<HTMLButtonElement>
// }

const CustomPrevArrow: React.FC<CustomArrowProps> = ({ className, onClick }) => {
    const t = useTranslations("TextForScreenReader.commentsArea")
    return (
        <button
            type='button'
            aria-label={t("prevButton")}
            className={className}
            onClick={onClick}
            style={{
                width: '30px',
                zIndex: 10,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: 'transparent',
                border: 'none',
                cursor: 'pointer'
            }}
        >
            <ArrowBigLeft color='white' size={50} />
        </button >
    )
}

const CustomNextArrow: React.FC<CustomArrowProps> = ({ className, onClick }) => {
    const t = useTranslations("TextForScreenReader.commentsArea")
    return (
        <button
            type='button'
            aria-label={t("nextButton")}
            className={className}
            onClick={onClick}
            style={{
                width: '30px',
                zIndex: 10,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: 'transparent',
                border: 'none',
                cursor: 'pointer'
            }}
        >
            <ArrowBigRight color='white' size={50} />
        </button >
    )
}

export default function SlideComments() {

    const t = useTranslations("MainPage.CommentsArea")

    const [slidesCount, setSlideCount] = useState<number | undefined>(undefined)
    useEffect(() => {
        const windowWidth = window.innerWidth
        setSlideCount(windowWidth <= 768 ? 1 : windowWidth <= 1024 ? 2 : 3)
    }, [slidesCount])

    const sliderSettings = {
        dots: true,
        infinite: true,
        slidesToShow: slidesCount,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 5000,
        pauseOnHover: true,
        prevArrow: <CustomPrevArrow />,
        nextArrow: <CustomNextArrow />,
    }

    if (!slidesCount) {
        return null
    }

    return (
        <section className={styles.testimonialArea}>
            <BreakupSection type={'up'} />
            <BreakupSection type={'down'} />
            <div className={styles.backgroundOverlay}></div>
            <div className={styles.backgroundOverlayImg}></div>
            <div>
                <div>
                    <div className={styles.sectionTitle}>
                        <h1>{t("title")}</h1>
                    </div>
                    <div className={styles.sliderContainer}>
                        <Slider {...sliderSettings}>
                            {commentInformation.map((item, index) => (
                                <Comment key={index} comment={item.comment} authorName={item.authorName} authorImg={item.authorImg} countStars={item.countStars} />
                            ))}
                        </Slider>
                    </div>
                </div>
            </div>
        </section>
    )
}