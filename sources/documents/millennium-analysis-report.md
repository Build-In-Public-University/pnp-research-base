# Fluid Blow-Up, AI, and the Shape of a Prediction

## Working news report and source-grounded analysis

Status: preliminary analysis of four local PDFs plus the Build In Public University post, “Temporal Dynamics: A Unified Solution to the Millennium Prize Problems.” This is not a peer review, a Lean audit, or a claim that the underlying theorems are false or accepted. It separates what the documents say from what can safely be reported.

## Bottom line

A serious mathematical advance is being presented inside a much larger story about AI-assisted research, credit, and a dispute over who knew what when.

The mathematical payload is narrower than the headline a casual reader might infer:

- Three released papers construct finite-time singularity/blow-up examples for forced fluid equations: incompressible porous media (IPM), two-dimensional inviscid Boussinesq, and three-dimensional incompressible Euler.
- The common technical move is to extend a Córdoba–Martínez-Zoroa multiscale program to smoother forcing and, for Euler, a genuinely three-dimensional axisymmetric-with-swirl setting.
- The forcing is not a cosmetic detail. It is an external term deliberately chosen to sustain the construction while remaining smooth. That makes these results mathematically meaningful, but it also means they are not the zero-force Navier–Stokes problem posed by Clay.
- The four-page statement says the authors believe they also have a hypodissipative Navier–Stokes blow-up result, but have not released it because Lean verification is unfinished and the write-up is not presentable.
- The statement openly says Claude, Codex, GPT-5.6 Sol, and Astra were used heavily. It also says the proof ideas came from the human researchers and, before them, Córdoba and Martínez-Zoroa.
- The older Temporal Dynamics post predicted the social and epistemic shape of this moment better than it predicted the mathematics: mathematical work as a temporal pipeline of exploration, verification, compression, and propagation. It did not predict this specific construction, authorship, tool chain, or credit conflict in a defensible technical sense.

The story is therefore not “AI solved the Millennium Problems.” It is:

> A human-led research program, developed over years, was pushed into harder forced-fluid regimes with large-language-model assistance. The resulting artifacts expose both a new research workflow and the unresolved cost of making machine-generated mathematics readable, attributable, and independently trusted.

## The cast

- Tristan Buckmaster and Levent Alpöge: authors of the three released papers and the public statement.
- Diego Córdoba and Luis Martínez-Zoroa: credited as originators of the underlying multiscale forced-blow-up program.
- Matei P. Coiculescu: third author on the IPM paper.
- Fan Zheng: cited in the surrounding research lineage on hypodissipative Navier–Stokes and unforced Euler; not an author of these three local papers.
- Claude, Codex, GPT-5.6 Sol, and Astra: AI systems used for ideation, proof iteration, bookkeeping, simplification, write-up, and auditing, according to the papers and statement.
- Lean: the proof assistant said to have verified the released Boussinesq and Euler proofs and, in the IPM paper, used as part of the formal-proof story. The local PDFs do not include the formal artifacts or a reproducible build receipt, so this report treats those claims as reported, not independently verified here.
- OpenAI personnel and an internal model: discussed only through Buckmaster’s account in the statement. The statement explicitly says he had not seen the alleged proof and was not accusing anyone of misuse of data.

## What each paper actually claims

### 1. IPM: the foundation and the upgrade

Title: “Extending the Córdoba-Martínez-Zoroa IPM Blow-Up to Uniformly Space-Time Smooth Forcing”
Authors: Levent Alpöge, Tristan Buckmaster, Matei P. Coiculescu
Local PDF: `Downloads/ipm.pdf`, 57 pages.

The theorem is on the two-dimensional torus T². It constructs smooth initial density and a force F that is C-infinity jointly in space and time on the closed interval [0,1]. The solution is smooth for every t<1, converges in every Hölder class C^η for η<1 to a limiting profile as t approaches 1, yet both the density gradient and the spatial gradient of the Darcy velocity diverge in L-infinity.

The paper identifies the inherited mechanism: a background flow amplifies higher-frequency oscillatory packets; each packet becomes a parent for the next scale; cutoffs, commutators, parametrices, and exact residual terms keep the forced equation honest. The new work claims a torus implementation with nested Fourier cutoffs, an exact cutoff commutator, a mixed time-space induction, and an exact series rather than a nonconstructive nonlinear limit. Its stated upgrade is uniform space-time smoothness of the force.

Why it matters: it makes the original Córdoba–Martínez-Zoroa phenomenon stronger in regularity and changes the domain from the whole plane to the torus. It is also the base layer for the Boussinesq and Euler extensions.

What it does not mean: IPM is not Navier–Stokes. It is an active scalar model driven by Darcy’s law. A blow-up result for forced IPM is evidence about a multiscale mechanism, not a solution to the Clay problem.

Useful local references: IPM PDF, pp. 1–3, Theorem 2.1 and the comparison immediately following it; AI statement at pp. 2–3 of the paper.

### 2. Boussinesq: smooth forcing on R²

Title: “Blowup for the Boussinesq Equations with Smooth Forcing”
Authors: Levent Alpöge and Tristan Buckmaster
Local PDF: `Downloads/boussinesq.pdf`, 76 pages.

The theorem constructs a finite-time singularity for the inviscid two-dimensional Boussinesq system on R². The initial temperature is smooth and compactly supported; the initial velocity is zero. Both forcing terms are smooth and compactly supported in space-time, with one fixed spatial ball containing the support. The temperature remains bounded, while its gradient tends to infinity and the vorticity has infinite limsup as the terminal time is approached. The solution is smooth and unique on every closed preterminal interval in the stated localized Biot–Savart class.

The mechanism is physically legible even if the proof is technical: the initial data create a smooth Rayleigh–Taylor-unstable stratification. Localized waves are added at successively shorter wavelengths. Their amplitudes can stay small while their gradients grow. The temperature gradient amplifies vorticity, and the new layer becomes the background for the next layer. Infinitely many stages are packed into finite time. The hard part is preventing cancellation in the state while keeping every derivative of the external forces controlled through blow-up.

The paper explicitly says the principal intellectual foundation is Córdoba and Martínez-Zoroa’s program. Its own contribution is the adaptation to Boussinesq with smooth compactly supported forcing, including the layer bookkeeping, exact correction equations, and common scale choices needed for all mixed derivatives. The audit burden is concentrated in the infinite frequency schedule, the return/steering selection, and the derivative estimates that make the force smooth at the endpoint.

What it does not mean: this is not a proof of singularity for unforced 2D Boussinesq, and it is not the Clay Navier–Stokes result. It is an inviscid, forced, two-dimensional system with a related but distinct structure.

AI disclosure: Section 2 says Claude and Codex were used to iterate proof ideas and writeups, with later work through 5.6 Sol and Astra. The authors say the final readable argument required their direction and hand editing. The wording about Lean is not a reproducible receipt: it refers to a first blow-up solution and does not provide source, theorem names, imports, or a build log sufficient to establish that this entire 76-page construction was kernel-checked.

Useful local references: pp. 1–3, Theorem 1.1; pp. 3–7, the layer mechanism; p. 7 onward, “AI statement.”

### 3. Euler: the headline mathematical result

Title: “Blowup for the Euler Equations with Smooth Forcing”
Authors: Levent Alpöge and Tristan Buckmaster
Local PDF: `Downloads/euler.pdf`, 112 pages.

The theorem constructs a finite-time singularity for the three-dimensional incompressible Euler equations on R³ with a force smooth in space and time up to the blow-up time. The construction is axisymmetric with swirl and supported in a fixed solid torus around an arbitrarily prescribed circle radius and height. The initial velocity is smooth, has nonzero swirl, and has zero meridional component. Circulation and meridional velocity remain bounded, while the circulation gradient and full vorticity diverge; the time integral of the L-infinity vorticity norm also diverges.

The proof uses cylindrical coordinates and a meridional reduction. A compact rotating base creates angular control. Localized circulation and velocity oscillations are transported by the complete preceding flow. Each new layer amplifies a small circulation seed, then returns its principal azimuthal-vorticity amplitude to zero before the next layer is introduced. Higher-order corrections make the physical force summable in every mixed derivative.

The authors place the result in a lineage that includes earlier forced Euler work with less regular forcing, unforced Euler constructions with C^{1,α} regularity and singularity away from one point, and the Boussinesq/IPM constructions. The paper claims that the present argument pushes the forced axisymmetric-with-swirl construction to smooth forcing and keeps a fixed compact support.

Why it matters: among the three papers, this is the clearest bridge toward the three-dimensional fluid-singularity frontier. It is also the easiest to misreport. “Euler blow-up” is not “Navier–Stokes solved,” and forced Euler is not unforced Euler.

AI disclosure: the separate four-page statement describes Claude and Codex in proof development and write-up, with author-directed iteration and hand editing. The statement is harsher about the presentation, calling the Euler write-up “AI slop.” I did not find a matching AI-disclosure or formal-verification section in the extracted Euler PDF itself. The local artifact also does not establish publication or peer-review status. These absences do not prove that no AI or formal tools were used; they mark what this PDF cannot document.

Useful local references: pp. 1–4, Theorem 1.1 and related work; pp. 4–10, coordinate reduction and mechanism; later sections for the correction and summability argument.

## The Clay boundary: where the headline must stop

Fefferman’s official problem description gives four acceptable targets. For Navier–Stokes, the existence alternatives (A) and (B) require positive viscosity, zero force, arbitrary smooth divergence-free initial data, and globally smooth physically reasonable solutions on R³ or the periodic quotient. The breakdown alternatives (C) and (D) allow a smooth external force, but they ask for a smooth initial field and force for which no global smooth solution exists.

The three released papers are not those statements:

- IPM is a different equation.
- Boussinesq is inviscid, two-dimensional, and forced.
- Euler has zero viscosity, three dimensions, and smooth forcing.
- The unreleased Navier–Stokes work is explicitly described as hypodissipative, not the standard positive-viscosity Clay equation, and its Lean verification is unfinished.

The papers are still relevant because forced problems can reveal mechanisms and techniques that may transfer to harder unforced regimes. But “suggestive of a path” is not “the path has been completed.” The statement itself makes that distinction.

## How much did the 2025 Temporal Dynamics post predict?

### Prediction scorecard

| Feature | In the old post? | Match to current work | Assessment |
|---|---:|---:|---|
| Mathematical work as a process unfolding in time | Yes | Medium | The new papers are explicitly a year-long research process with a rapid final month. This is a social/process match, not a theorem. |
| Exploration followed by algorithmic or formalized state | Yes | Medium-high | The papers describe LLM exploration, proof iteration, Lean checking, and human rewrite. The pipeline shape is close. |
| Verification as a bottleneck | Yes | High | Lean verification, readability, attribution, and independent review are central constraints. |
| A common cross-domain mechanism | Yes | Medium | The same multiscale layer program crosses IPM, Boussinesq, and Euler. But it is not the old post’s temporal entropy theory. |
| TNP → TP as a mathematical explanation of the problems | Yes | Low | The new proofs use PDE layers, transport, oscillation, and forcing estimates—not the temporal complexity classes proposed in the post. |
| A new theorem proving P ≠ NP | Yes | None | Nothing in these fluid papers bears on P versus NP. The old argument remains a category error: historical discovery time is not formal polynomial-time complexity. |
| AI generates the core result in a month | Broadly suggested | Partial | The statement says the decisive Boussinesq/Euler progress occurred around August 15 and Lean verification on August 22, after roughly a year of work. That is not a zero-context one-month solution. |
| Formal proof infrastructure changes credit and training | Yes | High | The statement says exactly this, comparing the moment to Deep Blue–Kasparov and asking how students, referees, and credit systems should adapt. |
| Public conflict over provenance and credit | Not clearly | High, but not predicted technically | The current dispute over rumors, OpenAI, authorship, and possible data access is part of the event’s social shape, but was not a consequence deduced by the old post. |

### Honest estimate

If “predicted the shape” means the workflow and institutional consequences, the post has a meaningful hit: perhaps 5–6 of 10 structural features. If it means predicting the actual mathematics, it predicted very little. The decisive mechanism was already present in the Córdoba–Martínez-Zoroa research program, not in the Temporal Dynamics post.

The strongest continuity is:

> discovery is not the same event as verification, and the rate-limiting step moves as the network changes.

The strongest discontinuity is:

> the papers’ mathematics is not temporal complexity theory. It is a carefully engineered forced-PDE construction.

That discontinuity should be stated on camera, because otherwise the report becomes a retrospective self-congratulation machine. The old post was directionally perceptive and technically overclaimed.

## The AI question: what changed, exactly?

The papers and statement describe a division of labor that is more interesting than the slogan “AI did the proof”:

1. Human researchers brought the research program, literature, target equations, and strategic constraints.
2. LLMs generated candidate proof architectures, identified or reproduced prior mechanisms, handled some bookkeeping, and proposed simplifications.
3. Humans rejected bad constructions, selected among alternatives, supplied corrections, and imposed direction.
4. Lean was reportedly used as a formal check, but the inspected PDFs do not provide public source, exact revisions, theorem names, or reproducible build receipts for the released arguments. The IPM paper specifically contains placeholder hashes for the Boussinesq/Euler artifacts and no Lean artifact for its own theorem.
5. Humans then faced the least glamorous part: understanding the generated argument and turning it into prose another mathematician could inspect.

This is not autonomous mathematics in the strong sense. It is a high-throughput human-machine research loop with formal verification in the middle and exposition still lagging behind.

The bottleneck therefore moved. Before, the scarce resource was often candidate construction. Now candidate constructions can be generated faster. The scarce resources become:

- choosing the right problem and route;
- distinguishing a real construction from a plausible-looking one;
- formalizing every dependency without smuggling in assumptions;
- making the proof human-readable;
- assigning credit across human ideas, model outputs, formal libraries, and prior literature;
- proving that private work was not improperly reused.

That is exactly where the old post’s “network configuration” intuition becomes useful—provided it is translated into measurable research infrastructure rather than treated as a proof of a new complexity class.

## News-story framing for YouTube

### Suggested headline

“AI Helped Push a Fluid-Dynamics Proof Forward. The Hard Part Is Still Knowing What Was Proved.”

### Alternate headline

“Not a Millennium Prize Solution: The AI-Assisted Fluid Blow-Up Results Behind This Week’s Math Shock.”

### Lede

A mathematician and an AI researcher have released three papers showing that carefully forced fluid equations can develop singularities in finite time. The work does not solve the Clay Institute’s Navier–Stokes problem. It does something more precise—and, in some ways, more revealing: it shows how a multiyear human research program can be extended with large language models, checked in Lean, and then arrive in public before the explanation is fully ready.

### Episode spine

1. Open on the misleading headline: “Did AI solve Navier–Stokes?”
2. Reset the facts: three released forced-fluid results; one unreleased hypodissipative Navier–Stokes claim.
3. Explain blow-up with one visual: a smooth-looking field whose gradient becomes infinite while the field itself can remain bounded.
4. Introduce the Córdoba–Martínez-Zoroa program as the real intellectual starting point.
5. Walk through the three papers: IPM as the base, Boussinesq as the buoyancy/layer extension, Euler as the three-dimensional axisymmetric-with-swirl extension.
6. Draw the Clay boundary: smooth forcing is not zero forcing; Euler is not Navier–Stokes.
7. Explain the AI workflow without mythology: generate, reject, formalize, understand, rewrite.
8. Cover the statement’s credit/provenance dispute as allegations, with the explicit caveat that the author says he has not seen OpenAI’s alleged proof and is not accusing anyone of data misuse.
9. Return to Temporal Dynamics: the old post got the pipeline and bottleneck shift right, but its Millennium-wide theorems were too ambitious.
10. End with the actual question: can mathematical institutions preserve understanding, credit, and training when proof search becomes cheap but proof explanation remains expensive?

### Visual vocabulary

- Three columns: equation / forcing / singular quantity.
- A ladder of spatial scales, each finer layer feeding the next.
- Green lane: “formal claim.” Red lane: “not established by these papers.”
- A Clay boundary card: “forced ≠ unforced; Euler ≠ Navier–Stokes.”
- A process diagram: human idea → model search → failed candidates → Lean check → human-readable proof.
- A provenance ledger with four labels: inherited mechanism, author adaptation, model assistance, independently verified outcome.

## Claims we should not make on camera

- “AI solved Navier–Stokes.”
- “The Millennium Problems have been solved.”
- “The old Temporal Dynamics post predicted these proofs.”
- “Lean verified that the papers are correct in every mathematical and editorial sense.”
- “OpenAI stole the work.” The statement reports allegations and unanswered questions; it does not establish data misuse or theft.
- “The papers are physically realistic because the forcing is smooth.” Smoothness is a mathematical regularity property, not a complete physical realism certificate.

## What would strengthen the story before publication

1. Obtain and archive the exact Lean repositories or certificates for each released result, with commit hashes and build output.
2. Check whether the formalization proves the exact theorem stated in the PDFs, rather than a related proposition.
3. Ask independent fluid-dynamics experts to classify the result’s novelty relative to Córdoba–Martínez-Zoroa and the other cited papers.
4. Preserve the unreleased Navier–Stokes claim as unverified until the paper, formalization, and exact equation/forcing regime are public.
5. Obtain OpenAI’s response to the specific timeline, authorship, prompt, compute, and data-retention questions before presenting the dispute as settled.
6. Put a visible correction box in the video description: “The results discussed are forced PDE constructions and do not settle the Clay Navier–Stokes problem.”

## Final interpretation

The old post was wrong in the way ambitious maps are often wrong: it confused a useful coordinate system with the territory. But it noticed something real. The future of research is likely to be shaped less by whether an AI can emit a plausible proof than by which networks can turn search into trusted, legible, attributable knowledge.

These papers are an early artifact of that transition. Their mathematics belongs to a specific lineage of fluid blow-up constructions. Their workflow belongs to a new human–AI research economy. Their public release shows the unresolved failure mode: the machine can accelerate the search, formal verification can check a formal object, and the human reader can still be left standing outside the proof with a very large document and a small amount of time.

The thesis means nothing without the artifact. Here the artifacts are real enough to study. The claims still need the rest of the pipeline.

## Sources

Local:

- `<HOME>/Downloads/boussinesq.pdf`
- `<HOME>/Downloads/euler.pdf`
- `<HOME>/Downloads/ipm.pdf`
- `<HOME>/Downloads/statement.pdf`

Public comparison and context:

- Build In Public University, “Temporal Dynamics: A Unified Solution to the Millennium Prize Problems”: https://www.buildinpublicuniversity.com/temporal-dynamics-a-unified-solution-to-the-millennium-prize-problems/
- Clay Mathematics Institute, Charles Fefferman, “Existence and Smoothness of the Navier–Stokes Equation”: https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf
- Córdoba and Martínez-Zoroa, “Finite time singularities of smooth solutions for the 2D incompressible porous media (IPM) equation with a smooth source”: https://doi.org/10.48550/arxiv.2410.22920
- Córdoba, Martínez-Zoroa, and Zheng, “Finite time blow-up for the hypodissipative Navier Stokes equations with a force…”: https://arxiv.org/abs/2407.06776
