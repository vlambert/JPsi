/*******************************************************************************
 * Test norm value caching in CINT for an example PDF 
 * Jan Veverka, Caltech, 9 February 2012
 ******************************************************************************/

// void phosphormodel5_test7() {
{
  RooWorkspace *w = new RooWorkspace("w", 1);
  w->factory("EXPR::model('1/((x-a)*(x-a)+0.01)+1/((y-a)*(y-a)+0.01)+"
	     "1/((z-a)*(z-a)+0.01)',x[-1,1],y[-1,1],z[-1,1],a[-5,5])") ;
  w->pdf("model")->setNormValueCaching(3) ;
  
  // Evaluate p.d.f. once to trigger filling of cache
  w->var("a")->setBins(10, "cache");
  RooArgSet normSet(*w->var("x"),*w->var("y"),*w->var("z")) ;
  w->pdf("model")->getVal(&normSet) ;

  }
