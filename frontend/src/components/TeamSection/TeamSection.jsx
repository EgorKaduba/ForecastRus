import "./TeamSection.css";
import teamPhoto from "../../assets/hero-team.jpg";
import crown from "../../assets/crown-egor.svg";
import starW from "../../assets/starW.svg";

function TeamSection() {
  return (
    <section className="team-section">
      <div className="team-photo">
        <img src={teamPhoto} alt="Команда из 5 разработчиков" />

        <div className="team-label group-backend">
          <div className="group-title">BACKEND-РАЗРАБОТЧИКИ</div>
          <div className="member-labels">
            <div className="member-label" id="max">
              <span className="member-name">МАКСИМ</span>
            </div>
            <div className="member-label" id="egor">
              <span id="teamlead">
                TEAM
                <br />
                LEAD
              </span>
              <div className="member-name-wrapper">
                <span className="member-name">ЕГОР</span>
                <img src={crown} id="crown" alt="crown" />
              </div>
            </div>
          </div>
        </div>

        <div className="team-label group-frontend">
          <div className="group-title">
            FRONTEND-РАЗРАБОТЧИКИ
            <br />
            ДИЗАЙНЕР
          </div>
          <div className="member-labels">
            <div className="member-label" id="vlada">
              <div className="member-name-wrapper">
                <span className="member-name">ВЛАДИСЛАВА</span>
                <img src={starW} id="star" alt="star" />
              </div>
            </div>
          </div>
        </div>

        <div className="team-label group-ml">
          <div className="group-title">ML-РАЗРАБОТЧИКИ</div>
          <div className="member-labels">
            <div className="member-label" id="danya">
              <span className="member-name">ДАНИЛА</span>
            </div>
            <div className="member-label" id="pasha">
              <span className="member-name">ПАВЕЛ</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default TeamSection;