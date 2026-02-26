<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CAPM® Exam Simulator 2026</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.2/babel.min.js"></script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { background: #0a0f1a; font-family: 'DM Sans', system-ui, sans-serif; color: white; min-height: 100vh; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
    button { font-family: 'DM Sans', system-ui, sans-serif; }
    #root { min-height: 100vh; }
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect, useRef } = React;

    // ─── Question Bank ────────────────────────────────────────────────────────
    const BASE_QUESTIONS = [
      { id:1,  domain:"Fundamentals",       question:"Which process group includes the Develop Project Charter process?",           options:["Initiating","Planning","Executing","Monitoring and Controlling"],                         correct:0, explanation:"Develop Project Charter is in the Initiating process group — it formally starts the project." },
      { id:2,  domain:"Fundamentals",       question:"A project is BEST defined as:",                                               options:["A repetitive operational process","A temporary endeavor creating unique deliverables","Ongoing business operations","A collection of related programs"], correct:1, explanation:"Projects are temporary (defined start/end) and produce unique deliverables, distinguishing them from operations." },
      { id:3,  domain:"Fundamentals",       question:"Which document formally authorizes a project?",                               options:["Project Management Plan","Project Charter","Business Case","Requirements Document"],          correct:1, explanation:"The Project Charter formally authorizes the project and grants the PM authority to apply resources." },
      { id:4,  domain:"Fundamentals",       question:"The triple constraint traditionally includes:",                                options:["Time, cost, quality","Scope, time, cost","Risk, quality, scope","Resources, time, risk"],   correct:1, explanation:"The triple constraint is scope, time, and cost — changes to one typically affect the others." },
      { id:5,  domain:"Fundamentals",       question:"A program is BEST described as:",                                             options:["A very large project","Related projects managed together for benefits","A strategic initiative only","Daily operational activities"], correct:1, explanation:"A program is a group of related projects managed in a coordinated way for strategic benefits." },
      { id:6,  domain:"Fundamentals",       question:"Who is responsible for authorizing the Project Charter?",                     options:["Project Manager","Sponsor or Initiator","PMO","Stakeholders"],                              correct:1, explanation:"The project sponsor or senior management authorizes the Project Charter." },
      { id:7,  domain:"Fundamentals",       question:"The PMBOK Guide defines a portfolio as:",                                     options:["A collection of programs only","Projects and programs aligned to strategic objectives","All active projects in an organization","A set of project templates"], correct:1, explanation:"A portfolio includes projects, programs, and operations managed as a group to achieve strategic objectives." },
      { id:8,  domain:"Fundamentals",       question:"Which process group involves developing the scope statement?",                options:["Initiating","Planning","Executing","Closing"],                                               correct:1, explanation:"Defining scope is a Planning process — you plan the scope before executing work." },
      { id:9,  domain:"Fundamentals",       question:"Organizational process assets (OPAs) include:",                              options:["Marketplace conditions","Lessons learned and historical data","Organizational structure","Government regulations"], correct:1, explanation:"OPAs are plans, processes, policies, templates, and historical knowledge from the organization." },
      { id:10, domain:"Fundamentals",       question:"Enterprise Environmental Factors (EEFs) include:",                           options:["Project templates","Organizational culture and market conditions","Lessons learned databases","Standard processes"], correct:1, explanation:"EEFs are conditions outside the project team's immediate control: culture, market, regulations, infrastructure." },
      { id:11, domain:"Predictive",         question:"What does SPI = 0.8 indicate?",                                              options:["Ahead of schedule","Behind schedule","On schedule","Over budget"],                           correct:1, explanation:"SPI < 1 means behind schedule. Only 80% of planned work has been completed." },
      { id:12, domain:"Predictive",         question:"The critical path is the:",                                                   options:["Shortest path through the network","Longest path — it determines project duration","Most expensive sequence of activities","Path with the highest risk"], correct:1, explanation:"The critical path is the longest path through the network, determining minimum project duration." },
      { id:13, domain:"Predictive",         question:"What is the formula for Earned Value (EV)?",                                  options:["AC × % Complete","BAC × % Complete","PV − AC","BAC − AC"],                                  correct:1, explanation:"EV = BAC × % Complete. It represents the budgeted value of work actually accomplished." },
      { id:14, domain:"Predictive",         question:"Cost Performance Index (CPI) = 1.2 means:",                                  options:["Over budget by 20%","Getting $1.20 of value per $1 spent","Behind schedule","Under budget by 20%"], correct:1, explanation:"CPI > 1 is favorable — the project gets more value than money spent. CPI = EV / AC." },
      { id:15, domain:"Predictive",         question:"Estimate at Completion (EAC) when original estimate is flawed:",             options:["BAC/CPI","AC + BAC − EV","AC + (BAC − EV)/CPI","AC + new estimate for remaining work"],    correct:3, explanation:"When the original estimate is flawed, EAC = AC + a new bottom-up estimate for remaining work." },
      { id:16, domain:"Predictive",         question:"A WBS is decomposed into:",                                                   options:["Activities and milestones","Work packages","Resources","Risk items"],                        correct:1, explanation:"WBS decomposition ends at work packages — the lowest level for reliable cost and duration estimates." },
      { id:17, domain:"Predictive",         question:"Float (slack) on the critical path equals:",                                  options:["Maximum delay allowed","Zero","A positive value","Depends on project"],                     correct:1, explanation:"Activities on the critical path have zero total float — any delay delays the entire project." },
      { id:18, domain:"Predictive",         question:"Which risk response strategy transfers risk to a third party?",              options:["Avoid","Transfer","Mitigate","Accept"],                                                      correct:1, explanation:"Transfer shifts the impact to a third party (e.g., insurance, outsourcing) but doesn't eliminate the risk." },
      { id:19, domain:"Agile",              question:"Who manages the Product Backlog in Scrum?",                                   options:["Scrum Master","Product Owner","Development Team","Project Manager"],                        correct:1, explanation:"The Product Owner is solely accountable for Product Backlog management and ordering." },
      { id:20, domain:"Agile",              question:"What is the maximum Sprint duration in Scrum?",                               options:["1 week","2 weeks","1 month","6 weeks"],                                                      correct:2, explanation:"The Scrum Guide states Sprints are one month or less to maintain consistency and reduce risk." },
      { id:21, domain:"Agile",              question:"The Agile Manifesto values 'Working software over':",                        options:["Comprehensive documentation","Customer collaboration","Responding to change","Individuals and interactions"], correct:0, explanation:"The second Agile value: working software over comprehensive documentation — though docs still have value." },
      { id:22, domain:"Agile",              question:"A Daily Scrum should be:",                                                    options:["30 minutes maximum","15 minutes or less","1 hour","As long as needed"],                     correct:1, explanation:"The Daily Scrum is time-boxed to 15 minutes for Developers to synchronize and plan the next 24 hours." },
      { id:23, domain:"Agile",              question:"What is a 'Definition of Done' in Scrum?",                                   options:["A list of Sprint backlog items","Formal criteria for an Increment to be releasable","User acceptance criteria","The Product Owner's approval"], correct:1, explanation:"The Definition of Done is a formal description of the state of the Increment when it meets quality measures." },
      { id:24, domain:"Agile",              question:"Velocity in Agile represents:",                                               options:["Team speed in lines of code","Amount of work completed per Sprint","Budget burn rate","Number of meetings held"], correct:1, explanation:"Velocity is the amount of work (story points) a team completes per Sprint, used for forecasting." },
      { id:25, domain:"Business Analysis",  question:"Requirements traceability is used to:",                                       options:["Track project costs","Link requirements to deliverables and business objectives","Create project schedules","Assign team resources"], correct:1, explanation:"Traceability links requirements from source to deliverables, enabling change impact assessment." },
      { id:26, domain:"Business Analysis",  question:"Which elicitation technique is best for stakeholders who can't articulate needs?", options:["Structured interviews","Observation (job shadowing)","Online surveys","Document analysis"], correct:1, explanation:"Observation lets the analyst see actual work performed and infer implicit requirements." },
      { id:27, domain:"Business Analysis",  question:"Functional requirements describe:",                                           options:["System performance constraints","What the system should do","How fast it should respond","Security requirements"], correct:1, explanation:"Functional requirements describe system behavior — what it must do in response to inputs or conditions." },
      { id:28, domain:"Business Analysis",  question:"A gap analysis compares:",                                                    options:["Budget vs. actuals","Current state vs. desired future state","Risk probability vs. impact","Planned vs. actual schedule"], correct:1, explanation:"Gap analysis identifies the difference between current and desired future state, informing solution requirements." },
      { id:29, domain:"Business Analysis",  question:"Which document captures all identified requirements?",                        options:["Project Charter","Requirements Traceability Matrix","Requirements Management Plan","Stakeholder Register"], correct:1, explanation:"The Requirements Traceability Matrix links each requirement to its source, status, and deliverables." },
      { id:30, domain:"Business Analysis",  question:"A use case describes:",                                                       options:["System architecture","How users interact with a system to achieve goals","Database schema","Technical specifications"], correct:1, explanation:"Use cases describe actor-system interactions that deliver value — focusing on goals, not implementation." },
    ];

    const QUESTIONS = [...BASE_QUESTIONS];
    while (QUESTIONS.length < 150) {
      const src = BASE_QUESTIONS[QUESTIONS.length % BASE_QUESTIONS.length];
      QUESTIONS.push({ ...src, id: QUESTIONS.length + 1, question: `[Practice] ${src.question}` });
    }

    const DC = { Fundamentals:"#6366f1", Predictive:"#0ea5e9", Agile:"#10b981", "Business Analysis":"#f59e0b" };
    const DOMAIN_WEIGHTS = { Fundamentals:36, Predictive:17, Agile:20, "Business Analysis":27 };

    function shuffle(arr) {
      const a = [...arr];
      for (let i = a.length-1; i > 0; i--) {
        const j = Math.floor(Math.random()*(i+1));
        [a[i],a[j]] = [a[j],a[i]];
      }
      return a;
    }
    function fmt(s) {
      const h=Math.floor(s/3600), m=Math.floor((s%3600)/60), sec=s%60;
      return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}`;
    }

    // ─── Timer Ring ───────────────────────────────────────────────────────────
    function TimerRing({ seconds, total }) {
      const pct = seconds / total;
      const color = pct > 0.5 ? "#10b981" : pct > 0.25 ? "#f59e0b" : "#ef4444";
      const size = 68, stroke = 5, r = (size - stroke*2)/2;
      const circ = 2*Math.PI*r;
      return (
        <div style={{position:"relative",display:"inline-flex",alignItems:"center",justifyContent:"center"}}>
          <svg width={size} height={size} style={{transform:"rotate(-90deg)"}}>
            <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth={stroke}/>
            <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth={stroke}
              strokeDasharray={circ} strokeDashoffset={circ*(1-pct)} strokeLinecap="round"
              style={{transition:"stroke-dashoffset 1s linear, stroke 0.5s"}}/>
          </svg>
          <span style={{position:"absolute",fontFamily:"'JetBrains Mono',monospace",fontSize:"9px",color:"white",letterSpacing:"-0.5px",textAlign:"center",lineHeight:1.2}}>
            {fmt(seconds)}
          </span>
        </div>
      );
    }

    // ─── Ambient BG ───────────────────────────────────────────────────────────
    function BG() {
      return (
        <div style={{position:"fixed",inset:0,pointerEvents:"none",zIndex:0,overflow:"hidden"}}>
          <div style={{position:"absolute",top:"-20%",left:"-10%",width:"60%",height:"60%",borderRadius:"50%",background:"radial-gradient(circle,rgba(99,102,241,0.07) 0%,transparent 70%)"}}/>
          <div style={{position:"absolute",bottom:"-10%",right:"-5%",width:"50%",height:"50%",borderRadius:"50%",background:"radial-gradient(circle,rgba(16,185,129,0.05) 0%,transparent 70%)"}}/>
        </div>
      );
    }

    // ─── Nav ──────────────────────────────────────────────────────────────────
    function Nav({ screen, setScreen }) {
      if (screen === "exam") return null;
      return (
        <nav style={{position:"sticky",top:0,zIndex:50,background:"rgba(10,15,26,0.88)",backdropFilter:"blur(12px)",borderBottom:"1px solid rgba(255,255,255,0.06)",padding:"0 24px"}}>
          <div style={{maxWidth:820,margin:"0 auto",display:"flex",alignItems:"center",height:52,gap:4}}>
            <span style={{fontFamily:"'Playfair Display',serif",color:"white",fontWeight:700,fontSize:17,marginRight:20,cursor:"pointer"}} onClick={()=>setScreen("home")}>CAPM®</span>
            {[["home","🏠 Home"],["study","📚 Study"],["review","📖 Review"]].map(([s,label])=>(
              <button key={s} onClick={()=>setScreen(s)} style={{background:screen===s?"rgba(99,102,241,0.15)":"transparent",border:screen===s?"1px solid rgba(99,102,241,0.3)":"1px solid transparent",borderRadius:8,padding:"6px 14px",color:screen===s?"#a78bfa":"#475569",fontSize:13,fontWeight:600,cursor:"pointer",transition:"all 0.15s"}}>
                {label}
              </button>
            ))}
          </div>
        </nav>
      );
    }

    // ─── Home ─────────────────────────────────────────────────────────────────
    function Home({ onStart, onStudy, onReview, lastResult }) {
      return (
        <div style={{maxWidth:700,margin:"0 auto",padding:"52px 24px"}}>
          <div style={{textAlign:"center",marginBottom:52}}>
            <div style={{display:"inline-block",background:"linear-gradient(135deg,#6366f1,#8b5cf6)",borderRadius:16,padding:"12px 20px",marginBottom:20}}>
              <span style={{fontSize:34}}>📋</span>
            </div>
            <h1 style={{fontFamily:"'Playfair Display',serif",fontSize:"clamp(2rem,5vw,3rem)",fontWeight:700,color:"white",lineHeight:1.1,margin:"0 0 12px"}}>
              CAPM® Exam<br/><span style={{color:"#a78bfa"}}>Simulator 2026</span>
            </h1>
            <p style={{color:"#64748b",fontSize:15,margin:0}}>150 questions · 3 hours · 4 knowledge domains</p>
          </div>

          <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:10,marginBottom:32}}>
            {Object.entries(DOMAIN_WEIGHTS).map(([d,w])=>(
              <div key={d} style={{background:"rgba(255,255,255,0.03)",border:"1px solid rgba(255,255,255,0.07)",borderRadius:12,padding:"16px 10px",textAlign:"center"}}>
                <div style={{width:8,height:8,borderRadius:"50%",background:DC[d],margin:"0 auto 8px"}}/>
                <div style={{color:"white",fontWeight:700,fontSize:22}}>{w}%</div>
                <div style={{color:"#475569",fontSize:11,marginTop:4,lineHeight:1.4}}>{d}</div>
              </div>
            ))}
          </div>

          <div style={{display:"grid",gap:10}}>
            <button onClick={onStart} style={{background:"linear-gradient(135deg,#6366f1,#4f46e5)",border:"none",borderRadius:12,padding:"18px 24px",color:"white",fontSize:16,fontWeight:700,cursor:"pointer",transition:"opacity 0.15s"}}
              onMouseOver={e=>e.currentTarget.style.opacity="0.88"} onMouseOut={e=>e.currentTarget.style.opacity="1"}>
              ⚡ Start Full Exam (150 Questions)
            </button>
            <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10}}>
              <button onClick={onStudy} style={{background:"rgba(255,255,255,0.04)",border:"1px solid rgba(255,255,255,0.09)",borderRadius:12,padding:"14px",color:"#94a3b8",fontSize:14,fontWeight:600,cursor:"pointer"}}>
                📚 Study Materials
              </button>
              <button onClick={onReview} style={{background:"rgba(255,255,255,0.04)",border:"1px solid rgba(255,255,255,0.09)",borderRadius:12,padding:"14px",color:"#94a3b8",fontSize:14,fontWeight:600,cursor:"pointer"}}>
                📖 Question Bank
              </button>
            </div>
          </div>

          {lastResult && (
            <div style={{marginTop:24,background:"rgba(99,102,241,0.08)",border:"1px solid rgba(99,102,241,0.2)",borderRadius:12,padding:"16px 20px"}}>
              <p style={{color:"#6366f1",fontSize:12,margin:"0 0 4px",fontWeight:700,textTransform:"uppercase",letterSpacing:1}}>Last Result</p>
              <p style={{color:"white",fontSize:22,fontWeight:700,margin:0}}>
                {lastResult.pct.toFixed(1)}% <span style={{color:"#475569",fontWeight:400,fontSize:14}}>({lastResult.correct}/{lastResult.total})</span>
                <span style={{marginLeft:12,fontSize:14,color:lastResult.passed?"#10b981":"#ef4444"}}>{lastResult.passed?"✓ Pass":"✗ Fail"}</span>
              </p>
            </div>
          )}
        </div>
      );
    }

    // ─── Study ────────────────────────────────────────────────────────────────
    function Study() {
      const [topic, setTopic] = useState("Fundamentals");
      const content = {
        Fundamentals: [
          { title:"Project Definition", body:"A project is a temporary endeavor with a defined beginning and end, undertaken to create a unique product, service, or result. Unlike operations, projects cease once objectives are met." },
          { title:"Process Groups (IPECC)", body:"Initiating → Planning → Executing → Monitoring & Controlling → Closing. M&C runs in parallel throughout all phases — not just at the end." },
          { title:"Organizational Structures", body:"Functional (PM low authority) → Weak Matrix → Balanced Matrix → Strong Matrix → Projectized (PM high authority). Structure impacts resource availability and PM power." },
          { title:"Portfolios, Programs & Projects", body:"Portfolio: strategic alignment. Program: benefit realization across related projects. Project: specific deliverable. Each level has distinct governance needs." },
        ],
        Predictive: [
          { title:"Earned Value Key Formulas", body:"EV = BAC × %Complete | CV = EV−AC | SV = EV−PV | CPI = EV/AC | SPI = EV/PV | EAC = BAC/CPI | ETC = EAC−AC | TCPI = (BAC−EV)/(BAC−AC)" },
          { title:"Critical Path Method", body:"Forward pass: ES + Duration − 1 = EF. Backward pass: LF − Duration + 1 = LS. Total Float = LS−ES or LF−EF. Critical path has zero float." },
          { title:"Risk Management", body:"Threat responses: Avoid, Transfer, Mitigate, Accept. Opportunity responses: Exploit, Share, Enhance, Accept. Residual risks remain after response; secondary risks arise from responses." },
          { title:"Quality Management", body:"Quality Planning → Quality Assurance (audit processes) → Quality Control (inspect deliverables). Prevention over inspection. Fishbone diagrams identify root causes." },
        ],
        Agile: [
          { title:"Scrum Framework", body:"Roles: Product Owner (backlog), Scrum Master (coach), Developers (build). Events: Sprint Planning, Daily Scrum (15 min), Sprint Review, Sprint Retrospective. Artifacts: Product Backlog, Sprint Backlog, Increment." },
          { title:"Agile Manifesto Values", body:"Individuals & interactions over processes & tools | Working software over comprehensive documentation | Customer collaboration over contract negotiation | Responding to change over following a plan" },
          { title:"Kanban Principles", body:"Visualize workflow, limit WIP, manage flow, make policies explicit, implement feedback loops. No prescribed roles or ceremonies unlike Scrum." },
          { title:"Hybrid Approaches", body:"Many organizations combine waterfall for planning/governance with sprints for execution. No single approach fits all projects — CAPM tests this understanding." },
        ],
        "Business Analysis": [
          { title:"Elicitation Techniques", body:"Interviews (targeted), Workshops/JAD (group consensus), Observation (implicit needs), Surveys (broad reach), Prototyping (visual feedback), Document analysis, Brainstorming." },
          { title:"Requirements Types", body:"Business (high-level goals) | Stakeholder (stakeholder needs) | Solution — Functional (what it does) & Non-functional (how well) | Transition (temporary migration needs)." },
          { title:"Requirements Traceability", body:"RTM links requirements → business objectives → WBS deliverables → test cases. Enables impact analysis when requirements change." },
          { title:"Modeling Techniques", body:"Use cases (actor-system interactions), User stories (As a... I want... So that...), Process flows (current vs future state), Entity relationship diagrams, State diagrams." },
        ],
      };
      return (
        <div style={{maxWidth:720,margin:"0 auto",padding:"32px 24px"}}>
          <h2 style={{fontFamily:"'Playfair Display',serif",color:"white",fontSize:28,marginBottom:24}}>Study Materials</h2>
          <div style={{display:"flex",gap:8,marginBottom:28,flexWrap:"wrap"}}>
            {Object.keys(content).map(t=>(
              <button key={t} onClick={()=>setTopic(t)} style={{background:topic===t?DC[t]:"rgba(255,255,255,0.04)",border:`1px solid ${topic===t?DC[t]:"rgba(255,255,255,0.09)"}`,borderRadius:8,padding:"8px 16px",color:"white",fontSize:13,fontWeight:600,cursor:"pointer",transition:"all 0.2s"}}>
                {t}
              </button>
            ))}
          </div>
          <div style={{display:"grid",gap:14}}>
            {content[topic].map((s,i)=>(
              <div key={i} style={{background:"rgba(255,255,255,0.03)",border:"1px solid rgba(255,255,255,0.06)",borderLeft:`3px solid ${DC[topic]}`,borderRadius:"0 12px 12px 0",padding:"16px 20px"}}>
                <h4 style={{color:"white",margin:"0 0 8px",fontSize:14,fontWeight:700}}>{s.title}</h4>
                <p style={{color:"#94a3b8",margin:0,fontSize:14,lineHeight:1.75}}>{s.body}</p>
              </div>
            ))}
          </div>
        </div>
      );
    }

    // ─── Review ───────────────────────────────────────────────────────────────
    function Review() {
      const [filter, setFilter] = useState("All");
      const [open, setOpen] = useState(null);
      const filtered = filter==="All" ? BASE_QUESTIONS : BASE_QUESTIONS.filter(q=>q.domain===filter);
      return (
        <div style={{maxWidth:720,margin:"0 auto",padding:"32px 24px"}}>
          <h2 style={{fontFamily:"'Playfair Display',serif",color:"white",fontSize:28,marginBottom:22}}>Question Bank</h2>
          <div style={{display:"flex",gap:8,marginBottom:22,flexWrap:"wrap"}}>
            {["All",...Object.keys(DOMAIN_WEIGHTS)].map(d=>(
              <button key={d} onClick={()=>setFilter(d)} style={{background:filter===d?(d==="All"?"#6366f1":DC[d]):"rgba(255,255,255,0.04)",border:`1px solid ${filter===d?(d==="All"?"#6366f1":DC[d]):"rgba(255,255,255,0.09)"}`,borderRadius:8,padding:"7px 14px",color:"white",fontSize:12,fontWeight:600,cursor:"pointer"}}>
                {d}
              </button>
            ))}
          </div>
          <div style={{display:"grid",gap:8}}>
            {filtered.map(q=>(
              <div key={q.id} style={{background:"rgba(255,255,255,0.03)",border:"1px solid rgba(255,255,255,0.07)",borderRadius:12,overflow:"hidden"}}>
                <button onClick={()=>setOpen(open===q.id?null:q.id)} style={{width:"100%",background:"none",border:"none",padding:"14px 16px",cursor:"pointer",textAlign:"left",display:"flex",alignItems:"center",gap:12}}>
                  <span style={{background:DC[q.domain],borderRadius:6,padding:"2px 8px",fontSize:10,fontWeight:700,color:"white",whiteSpace:"nowrap",flexShrink:0}}>{q.domain}</span>
                  <span style={{color:"#94a3b8",fontSize:13,flex:1,textAlign:"left"}}>{q.question}</span>
                  <span style={{color:"#475569",fontSize:16,flexShrink:0}}>{open===q.id?"−":"+"}</span>
                </button>
                {open===q.id&&(
                  <div style={{padding:"0 16px 16px",borderTop:"1px solid rgba(255,255,255,0.05)"}}>
                    {q.options.map((opt,j)=>(
                      <div key={j} style={{display:"flex",alignItems:"center",gap:10,padding:"8px 12px",borderRadius:8,marginTop:6,background:j===q.correct?"rgba(16,185,129,0.08)":"rgba(255,255,255,0.02)",border:`1px solid ${j===q.correct?"rgba(16,185,129,0.25)":"rgba(255,255,255,0.05)"}`}}>
                        <span style={{fontWeight:700,fontSize:12,color:j===q.correct?"#10b981":"#475569",minWidth:16}}>{String.fromCharCode(65+j)}</span>
                        <span style={{color:j===q.correct?"#6ee7b7":"#64748b",fontSize:13}}>{opt}</span>
                        {j===q.correct&&<span style={{marginLeft:"auto",color:"#10b981",fontSize:11}}>✓ Correct</span>}
                      </div>
                    ))}
                    <div style={{marginTop:12,padding:"10px 14px",background:"rgba(99,102,241,0.08)",borderRadius:8,borderLeft:"3px solid #6366f1"}}>
                      <p style={{color:"#a78bfa",fontSize:13,margin:0}}>💡 {q.explanation}</p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      );
    }

    // ─── Exam ─────────────────────────────────────────────────────────────────
    function Exam({ onFinish }) {
      const [questions] = useState(()=>shuffle(QUESTIONS));
      const [current, setCurrent] = useState(0);
      const [answers, setAnswers] = useState({});
      const [selected, setSelected] = useState(null);
      const [flagged, setFlagged] = useState(new Set());
      const [showNav, setShowNav] = useState(false);
      const [timeLeft, setTimeLeft] = useState(180*60);
      const [done, setDone] = useState(false);
      const TOTAL = 180*60;
      const timerRef = useRef(null);

      useEffect(()=>{
        timerRef.current = setInterval(()=>{
          setTimeLeft(s=>{
            if(s<=1){ clearInterval(timerRef.current); handleSubmit(true); return 0; }
            return s-1;
          });
        },1000);
        return ()=>clearInterval(timerRef.current);
      },[]);

      function handleSubmit(auto=false) {
        clearInterval(timerRef.current);
        const final = selected!==null ? {...answers,[current]:selected} : {...answers};
        const correct = questions.reduce((acc,q,i)=>acc+(final[i]===q.correct?1:0),0);
        onFinish({correct,total:questions.length,answers:final,questions});
      }

      function go(idx) {
        if(selected!==null) setAnswers(p=>({...p,[current]:selected}));
        const saved = answers[idx];
        setSelected(saved!==undefined?saved:null);
        setCurrent(idx);
        setShowNav(false);
      }

      const q = questions[current];
      const answered = Object.keys(answers).length + (selected!==null&&!(current in answers)?1:0);
      const pct = timeLeft/TOTAL;
      const timerColor = pct>0.5?"#10b981":pct>0.25?"#f59e0b":"#ef4444";

      return (
        <div style={{minHeight:"100vh",display:"flex",flexDirection:"column"}}>
          {/* Top bar */}
          <div style={{position:"sticky",top:0,zIndex:50,background:"rgba(10,15,26,0.92)",backdropFilter:"blur(12px)",borderBottom:"1px solid rgba(255,255,255,0.06)",padding:"10px 24px"}}>
            <div style={{maxWidth:820,margin:"0 auto",display:"flex",alignItems:"center",gap:16,flexWrap:"wrap"}}>
              <span style={{fontFamily:"'Playfair Display',serif",color:"white",fontWeight:700,fontSize:15}}>CAPM®</span>
              <div style={{flex:1}}>
                <div style={{height:3,background:"rgba(255,255,255,0.06)",borderRadius:2}}>
                  <div style={{height:"100%",width:`${(current/150)*100}%`,background:"linear-gradient(90deg,#6366f1,#8b5cf6)",borderRadius:2,transition:"width 0.3s ease"}}/>
                </div>
                <div style={{display:"flex",justifyContent:"space-between",marginTop:4}}>
                  <span style={{color:"#475569",fontSize:11}}>Question {current+1} of 150</span>
                  <span style={{color:"#475569",fontSize:11}}>{answered} answered</span>
                </div>
              </div>
              <TimerRing seconds={timeLeft} total={TOTAL}/>
            </div>
          </div>

          {/* Question */}
          <div style={{maxWidth:820,margin:"0 auto",width:"100%",padding:"28px 24px 100px",flex:1}}>
            <div style={{display:"flex",gap:10,marginBottom:16,flexWrap:"wrap"}}>
              <span style={{background:DC[q.domain],borderRadius:6,padding:"3px 10px",fontSize:11,fontWeight:700,color:"white"}}>{q.domain}</span>
              {flagged.has(current)&&<span style={{background:"rgba(245,158,11,0.12)",border:"1px solid rgba(245,158,11,0.3)",borderRadius:6,padding:"3px 10px",fontSize:11,color:"#f59e0b"}}>🚩 Flagged</span>}
            </div>

            <div style={{background:"rgba(255,255,255,0.03)",border:"1px solid rgba(255,255,255,0.07)",borderRadius:16,padding:"26px 26px 22px",marginBottom:18}}>
              <p style={{color:"white",fontSize:17,lineHeight:1.75,margin:0,fontWeight:500}}>{q.question}</p>
            </div>

            <div style={{display:"grid",gap:10,marginBottom:22}}>
              {q.options.map((opt,i)=>{
                const isSel = selected===i;
                const isSaved = answers[current]===i && !isSel;
                return (
                  <button key={i} onClick={()=>setSelected(i)} style={{background:isSel?"rgba(99,102,241,0.14)":isSaved?"rgba(99,102,241,0.07)":"rgba(255,255,255,0.02)",border:`1.5px solid ${isSel?"#6366f1":isSaved?"rgba(99,102,241,0.4)":"rgba(255,255,255,0.07)"}`,borderRadius:12,padding:"13px 16px",cursor:"pointer",textAlign:"left",display:"flex",alignItems:"center",gap:14,transition:"all 0.15s"}}
                    onMouseOver={e=>{if(!isSel)e.currentTarget.style.borderColor="rgba(99,102,241,0.35)";}}
                    onMouseOut={e=>{if(!isSel)e.currentTarget.style.borderColor=isSaved?"rgba(99,102,241,0.4)":"rgba(255,255,255,0.07)";}}>
                    <span style={{width:28,height:28,borderRadius:8,border:`2px solid ${isSel?"#6366f1":"rgba(255,255,255,0.14)"}`,background:isSel?"#6366f1":"transparent",display:"flex",alignItems:"center",justifyContent:"center",fontWeight:700,fontSize:12,color:isSel?"white":"#475569",flexShrink:0}}>{String.fromCharCode(65+i)}</span>
                    <span style={{color:isSel?"white":"#94a3b8",fontSize:14,lineHeight:1.5}}>{opt}</span>
                  </button>
                );
              })}
            </div>

            {/* Actions */}
            <div style={{display:"flex",gap:10,alignItems:"center",flexWrap:"wrap"}}>
              <button onClick={()=>setFlagged(s=>{const n=new Set(s);n.has(current)?n.delete(current):n.add(current);return n;})} style={{background:flagged.has(current)?"rgba(245,158,11,0.12)":"rgba(255,255,255,0.04)",border:`1px solid ${flagged.has(current)?"rgba(245,158,11,0.35)":"rgba(255,255,255,0.08)"}`,borderRadius:8,padding:"10px 16px",color:flagged.has(current)?"#f59e0b":"#64748b",fontSize:13,cursor:"pointer"}}>
                🚩 {flagged.has(current)?"Unflag":"Flag"}
              </button>
              <button onClick={()=>setShowNav(s=>!s)} style={{background:"rgba(255,255,255,0.04)",border:"1px solid rgba(255,255,255,0.08)",borderRadius:8,padding:"10px 16px",color:"#94a3b8",fontSize:13,cursor:"pointer"}}>
                ⊞ Navigator
              </button>
              <div style={{flex:1}}/>
              {current>0&&<button onClick={()=>go(current-1)} style={{background:"rgba(255,255,255,0.05)",border:"1px solid rgba(255,255,255,0.1)",borderRadius:8,padding:"10px 20px",color:"#94a3b8",fontSize:14,cursor:"pointer"}}>← Prev</button>}
              {current<149
                ?<button onClick={()=>go(current+1)} style={{background:"linear-gradient(135deg,#6366f1,#4f46e5)",border:"none",borderRadius:8,padding:"10px 24px",color:"white",fontSize:14,fontWeight:700,cursor:"pointer"}}>Next →</button>
                :<button onClick={()=>handleSubmit()} style={{background:"linear-gradient(135deg,#059669,#047857)",border:"none",borderRadius:8,padding:"10px 24px",color:"white",fontSize:14,fontWeight:700,cursor:"pointer"}}>✓ Submit</button>
              }
            </div>

            {/* Navigator */}
            {showNav&&(
              <div style={{marginTop:22,background:"rgba(10,15,26,0.95)",border:"1px solid rgba(255,255,255,0.08)",borderRadius:16,padding:20}}>
                <p style={{color:"#475569",fontSize:11,margin:"0 0 14px",textTransform:"uppercase",letterSpacing:1,fontWeight:600}}>Question Navigator</p>
                <div style={{display:"flex",flexWrap:"wrap",gap:5}}>
                  {questions.map((_,i)=>{
                    const done=answers[i]!==undefined||(i===current&&selected!==null);
                    const isCur=i===current;
                    const isFlag=flagged.has(i);
                    return (
                      <button key={i} onClick={()=>go(i)} style={{width:32,height:32,borderRadius:7,fontSize:10,fontWeight:600,cursor:"pointer",border:"1.5px solid",background:isCur?"#6366f1":done?"rgba(16,185,129,0.12)":"rgba(255,255,255,0.03)",borderColor:isCur?"#6366f1":isFlag?"#f59e0b":done?"rgba(16,185,129,0.35)":"rgba(255,255,255,0.08)",color:isCur?"white":done?"#6ee7b7":"#475569"}}>
                        {i+1}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        </div>
      );
    }

    // ─── Results ──────────────────────────────────────────────────────────────
    function Results({ result, onRetry, onHome }) {
      const { correct, total, answers, questions } = result;
      const pct = (correct/total)*100;
      const passed = pct >= 61;
      const [showWrong, setShowWrong] = useState(false);

      const domainStats = {};
      questions.forEach((q,i)=>{
        if(!domainStats[q.domain]) domainStats[q.domain]={correct:0,total:0};
        domainStats[q.domain].total++;
        if(answers[i]===q.correct) domainStats[q.domain].correct++;
      });
      const wrong = questions.map((q,i)=>({q,i,yours:answers[i]})).filter(x=>x.yours!==x.q.correct);

      return (
        <div style={{maxWidth:720,margin:"0 auto",padding:"44px 24px"}}>
          <div style={{textAlign:"center",marginBottom:48}}>
            <div style={{fontSize:52,marginBottom:14}}>{passed?"🎉":"📈"}</div>
            <h2 style={{fontFamily:"'Playfair Display',serif",fontSize:"clamp(1.8rem,5vw,2.6rem)",color:"white",margin:"0 0 8px"}}>{passed?"Congratulations!":"Keep Practicing"}</h2>
            <p style={{color:"#64748b",fontSize:15,margin:"0 0 32px"}}>{passed?"You passed the simulation!":"Review the domain breakdown below to improve"}</p>
            <div style={{display:"inline-flex",alignItems:"center",justifyContent:"center",width:156,height:156,borderRadius:"50%",background:`conic-gradient(${passed?"#10b981":"#6366f1"} ${pct*3.6}deg, rgba(255,255,255,0.05) 0deg)`,boxShadow:`0 0 40px ${passed?"rgba(16,185,129,0.25)":"rgba(99,102,241,0.25)"}`}}>
              <div style={{width:118,height:118,borderRadius:"50%",background:"#0a0f1a",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center"}}>
                <span style={{fontSize:30,fontWeight:800,color:"white"}}>{pct.toFixed(1)}%</span>
                <span style={{color:"#475569",fontSize:12}}>{correct}/{total}</span>
              </div>
            </div>
          </div>

          <h3 style={{color:"#64748b",fontSize:12,textTransform:"uppercase",letterSpacing:1,fontWeight:600,marginBottom:12}}>Domain Breakdown</h3>
          <div style={{display:"grid",gap:10,marginBottom:32}}>
            {Object.entries(domainStats).map(([domain,stat])=>{
              const dp=(stat.correct/stat.total)*100;
              return (
                <div key={domain} style={{background:"rgba(255,255,255,0.03)",border:"1px solid rgba(255,255,255,0.07)",borderRadius:12,padding:"13px 18px",display:"flex",alignItems:"center",gap:14}}>
                  <div style={{width:9,height:9,borderRadius:"50%",background:DC[domain],flexShrink:0}}/>
                  <span style={{color:"#94a3b8",fontSize:13,flex:1}}>{domain}</span>
                  <span style={{color:"white",fontWeight:700,fontSize:14}}>{dp.toFixed(0)}%</span>
                  <span style={{color:"#475569",fontSize:12}}>{stat.correct}/{stat.total}</span>
                  <div style={{width:72,height:4,background:"rgba(255,255,255,0.06)",borderRadius:2}}>
                    <div style={{width:`${dp}%`,height:"100%",background:DC[domain],borderRadius:2}}/>
                  </div>
                </div>
              );
            })}
          </div>

          <button onClick={()=>setShowWrong(s=>!s)} style={{width:"100%",background:"rgba(255,255,255,0.04)",border:"1px solid rgba(255,255,255,0.08)",borderRadius:10,padding:"12px 20px",color:"#94a3b8",fontSize:14,cursor:"pointer",marginBottom:20}}>
            {showWrong?"Hide":"Review"} Incorrect Answers ({wrong.length})
          </button>

          {showWrong&&(
            <div style={{display:"grid",gap:10,marginBottom:28}}>
              {wrong.map(({q,i,yours})=>(
                <div key={i} style={{background:"rgba(239,68,68,0.04)",border:"1px solid rgba(239,68,68,0.14)",borderRadius:12,padding:16}}>
                  <p style={{color:"#cbd5e1",fontSize:13,margin:"0 0 10px",fontWeight:500}}>{q.question}</p>
                  <div style={{display:"flex",gap:8,marginBottom:8,flexWrap:"wrap"}}>
                    <span style={{fontSize:11,padding:"3px 9px",borderRadius:5,background:"rgba(239,68,68,0.12)",color:"#f87171",border:"1px solid rgba(239,68,68,0.2)"}}>
                      Your: {yours!==undefined?q.options[yours]:"Unanswered"}
                    </span>
                    <span style={{fontSize:11,padding:"3px 9px",borderRadius:5,background:"rgba(16,185,129,0.1)",color:"#6ee7b7",border:"1px solid rgba(16,185,129,0.2)"}}>
                      ✓ {q.options[q.correct]}
                    </span>
                  </div>
                  <p style={{color:"#818cf8",fontSize:12,margin:0}}>💡 {q.explanation}</p>
                </div>
              ))}
            </div>
          )}

          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12}}>
            <button onClick={onRetry} style={{background:"linear-gradient(135deg,#6366f1,#4f46e5)",border:"none",borderRadius:12,padding:16,color:"white",fontSize:15,fontWeight:700,cursor:"pointer"}}>⚡ Retry Exam</button>
            <button onClick={onHome} style={{background:"rgba(255,255,255,0.05)",border:"1px solid rgba(255,255,255,0.1)",borderRadius:12,padding:16,color:"#94a3b8",fontSize:15,fontWeight:600,cursor:"pointer"}}>🏠 Home</button>
          </div>
        </div>
      );
    }

    // ─── App ──────────────────────────────────────────────────────────────────
    function App() {
      const [screen, setScreen] = useState("home");
      const [result, setResult] = useState(null);
      const [lastResult, setLastResult] = useState(null);

      function handleFinish(r) {
        const pct = (r.correct/r.total)*100;
        setLastResult({...r, pct, passed: pct>=61});
        setResult(r);
        setScreen("results");
      }

      return (
        <div style={{minHeight:"100vh",background:"#0a0f1a",fontFamily:"'DM Sans',system-ui,sans-serif"}}>
          <BG/>
          <div style={{position:"relative",zIndex:1}}>
            <Nav screen={screen} setScreen={setScreen}/>
            {screen==="home"    && <Home onStart={()=>setScreen("exam")} onStudy={()=>setScreen("study")} onReview={()=>setScreen("review")} lastResult={lastResult}/>}
            {screen==="study"   && <Study/>}
            {screen==="review"  && <Review/>}
            {screen==="exam"    && <Exam onFinish={handleFinish}/>}
            {screen==="results" && result && <Results result={result} onRetry={()=>setScreen("exam")} onHome={()=>setScreen("home")}/>}
          </div>
        </div>
      );
    }

    ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
  </script>
</body>
</html>
