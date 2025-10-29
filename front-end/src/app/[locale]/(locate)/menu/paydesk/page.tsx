import Header from '@/components/Header/Header/Header'
import ProductsCheck from '@/components/Paydesk/ProductsCheck'


export default function Paydesk() {

    return (
        <>
            <Header dataImg={'/Menu/background/bg.jpg'} isActiveHeader={'off'} isButton={'off'} />
            <ProductsCheck />

        </>
    )
}