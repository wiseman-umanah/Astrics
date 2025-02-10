gsap.registerPlugin(ScrollTrigger);

// You can use a ScrollTrigger in a tween or timeline
let tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".desc",
    start: "top bottom",
    end: "bottom top",
    scrub: true,
    id: "scrub"
  } 
})
tl.to(".desc", {
  duration: 1,
  rotation: 360,
})
.to(".desc", {
  duration: 2,
});


// header scroll
const showAnim = gsap.from('header', { 
	yPercent: -100,
	paused: true,
	duration: 0.2
  }).progress(1);
  
  ScrollTrigger.create({
	start: "top top",
	end: "max",
	onUpdate: (self) => {
	  self.direction === -1 ? showAnim.play() : showAnim.reverse()
	}
  });

