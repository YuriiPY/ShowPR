'use client'

import Image from 'next/image'

import styles from './Comment.module.scss'

interface Comment {
    comment: string,
    authorName: string,
    authorImg: string,
    countStars: number
}

export default function Comment({ comment, authorName, authorImg, countStars }: Comment) {

    const starList = []
    for (let i = 0; i <= countStars; i++) {
        starList.push(<div key={i} className={styles.star} ></div >)
    }
    return (
        <div className={styles.singleCarousel}>
            < div className={styles.authorOpinion} >
                <p>{comment}</p>
            </div >
            <div className={styles.testimonialAuthor} >
                <div className={styles.authorPhoto} >
                    <Image src={authorImg} alt='author image' width={60} height={60} />
                </div>
                <div className={styles.authorName} >
                    <h1>{authorName}</h1>
                    <div className={styles.icon} >
                        {starList}
                    </div >
                </div >
            </div >
        </div >
    )
}