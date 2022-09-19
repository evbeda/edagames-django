import './Galery.css'
import imagen_login from '../../images/imagen_ofi.jpeg'

export const Galery = () =>{
    return(
        <section className="container_galery">
            <img 
                className="image_background"
                src={imagen_login}
                alt="logo"
            />
        </section>
    )
}