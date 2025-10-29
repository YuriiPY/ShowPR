import SlideComments from '@/components/CommentsArea/SlideComments/SlideComments'
import Gallery from '@/components/Gallery/Gallery'
import Header from '@/components/Header/Header/Header'
import AboutArea from '@/components/MainArea/AboutArea/AboutArea'

const dataImg = [
    {
        url: '/MainPage/background/home_photo1.jpg'
    },
    {
        url: '/MainPage/background/home_photo2.jpg'
    },
    {
        url: '/MainPage/background/home_photo3.jpg'
    }
]

export default function MainPage() {
    return (
        <main
            role='main'
            aria-label='Strona internetowa Alina pierogowa'
        >
            <Header dataImg={dataImg} isActiveHeader={'on'} isButton={'on'} />
            <AboutArea />
            <SlideComments />
            <Gallery />
        </main>
    )
}	