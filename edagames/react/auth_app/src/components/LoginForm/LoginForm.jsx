import './LoginForm.css'
import { GrLinkedin } from "react-icons/gr";
import logo_eda from '../../images/edagames_logo.jpeg'

export const LoginForm = () =>{
    return(
        <section className = "container">
            <img  
                className="image"
                src={logo_eda} 
                alt="logo"
            />
            <h2 className = "title">
                Welcome to EDA Games!
            </h2>
            <section className="form_login">
                <button 
                    onClick={()=>{
                        window.location.href ="/oauth/login/linkedin-oauth2/"
                    }} 
                    className='button_login'
                >
                    <GrLinkedin className='icons'/>
                    Login with LinkedIn
                </button>
            </section>
        </section>
    )
}