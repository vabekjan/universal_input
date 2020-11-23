module libraries

use util; 

IMPLICIT NONE;

CONTAINS

integer FUNCTION multiprod(l,n_drive); !=prod_k=1^l n_drive(k)
 integer, intent(in) :: l;
 integer, dimension(:), intent(in) :: n_drive;
 integer :: k1;
	
	multiprod=1.0d0;
	do k1 = 1, l
		multiprod = multiprod*n_drive(k1)	
	enddo

end function multiprod; 


recursive subroutine increase(k,n_drive,setup) !!! No debugging, i.e. a correct input has to be used
 integer, intent(in) :: k;
 integer, dimension(:), intent(in) :: n_drive;
 integer, dimension(:) :: setup;
 
	if (setup(k) == n_drive(k) ) then
		setup(k) = 1;
		call increase(k+1,n_drive,setup)
	else
	setup(k)=setup(k) + 1;
	endif
	
end subroutine increase;


integer FUNCTION filelength(cwd); !
	character(255), intent(in) :: cwd;

	character(255) :: cwd1;
	integer :: IO, k, N_load;
	
	cwd1=TRIM(cwd)
!	write(*,*) cwd;
!	write(*,*) cwd1;
	open(UNIT=1,FILE=cwd1,FORM="FORMATTED",action='read');
	N_load = 0; IO = 0;
		do while(IO >= 0)
			read(1,*,IOSTAT = IO); N_load = N_load+1; 
		enddo
	close(1);
 	N_load = N_load - 1; !# of lines in the loaded file
	filelength = N_load;

end function filelength; 


subroutine loadfile2(cwd,N_vec,vec) !load a file with real*8 values, uses unit=1 !!!
 character(255), intent(in) :: cwd;
 real*8, dimension(:), allocatable, intent(out) :: vec;
 integer, intent(in) :: N_vec;
 integer :: N_load, IO, k;
 character(255) :: cwd1;

	cwd1=TRIM(cwd)
	open(UNIT=1,FILE=cwd1,FORM="FORMATTED",action='read');

	allocate(vec(1:N_vec)); 

	!reading the file
	do k = 1 , N_vec
		read(1,*) vec(k);
	enddo
	close(1);
end subroutine loadfile2;



subroutine loadfile(cwd,N_vec,vec) !load a file with real*8 values, uses unit=1 !!!
 character(255), intent(in) :: cwd;
 real*8, dimension(:), allocatable, intent(out) :: vec;
 integer, intent(out) :: N_vec;
 integer :: N_load, IO, k;
 character(255) :: cwd1;

	cwd1=TRIM(cwd)
	open(UNIT=1,FILE=cwd1,FORM="FORMATTED",action='read');
	N_load = 0; IO = 0;
		do while(IO >= 0)
			read(1,*,IOSTAT = IO); N_load = N_load+1; 
		enddo
 	N_load = N_load - 1; !# of lines in the loaded file

	!allocation of proper variables
	N_vec=N_load;
	allocate(vec(1:N_vec)); 

	!reading the file
	rewind(unit=1,iostat=IO);
	do k = 1 , N_vec
		read(1,*) vec(k);
	enddo
	close(1);
end subroutine loadfile;


subroutine interpolate(n,x,y,x_grid,y_grid) !inputs: # of points, x(n), y(x(n)), x, returns y(x) (linearinterpolation), extrapolation by the boundary values

	integer, intent(in)  :: n
	real*8, intent(in)  :: x, x_grid(n), y_grid(n)
 	real*8 :: y; ! output	
	integer :: k1,k2;
	
	call findinterval(n,x,x_grid,k1,k2);
	!write(*,*) k1;
	if ( k1==0 ) then
		y=y_grid(1);
	elseif ( k2 == 0 ) then
		y=y_grid(n);
	else
		y=y_grid(k1)+(x-x_grid(k1))*(y_grid(k2)-y_grid(k1))/(x_grid(k2)-x_grid(k1));
	endif

end subroutine interpolate

subroutine interpolate2n(n,x,y,x_grid,y_grid) !inputs: # of points is 2^n, x(n), y(x(n)), x, returns y(x) (linearinterpolation), extrapolation by the boundary values

	integer, intent(in)  :: n
	real*8, intent(in)  :: x, x_grid(n), y_grid(n)
 	real*8 :: y; ! output	
	integer :: k1,k2;
	
	call findinterval2n(n,x,x_grid,k1,k2);
	!write(*,*) k1;
	if ( k1 == 0 ) then
		y=y_grid(1);
	elseif ( k2 == 0 ) then
		y=y_grid(n);
	else
		y=y_grid(k1)+(x-x_grid(k1))*(y_grid(k2)-y_grid(k1))/(x_grid(k2)-x_grid(k1));
	endif

end subroutine interpolate2n;

subroutine findinterval(n,x,x_grid,k1,k2) ! returns interval where is placed x value, if it is out of the range, 0 is used
!intervals are ordered: <..>(..>(..>...(..>
	integer, intent(in)  :: n
	real*8, intent(in)  :: x, x_grid(n)
 	integer, intent(out) :: k1,k2; ! output
	integer :: i;
	
	
	if ( x < x_grid(1) ) then
			k1 = 0;
			k2= 1;
			return;
	endif

	do i = 1 , (n-1)
		if ( x <= x_grid(i+1) ) then
			k1 = i;
			k2= i+1;
			return;
		endif
	enddo

 	k1=n; k2=0;

	!write(*,*) "error in the interval subroutine"
end subroutine findinterval

subroutine findinterval2n(n,x,x_grid,k1,k2) ! returns first point of interval where is x o for 2^n grid
!intervals are ordered: <..>(..>(..>...(..>
	integer, intent(in)  :: n ! # of points is 2^n
	real*8, intent(in)  :: x, x_grid(n)
 	integer, intent(out) :: k1,k2 ! output
	integer :: i,k;

	if ( x < x_grid(1) ) then
			k1 = 0;
			k2= 1;
			write(*,*) "interpolation out of range (left)";
			return;
	elseif ( x > x_grid(2**n) ) then
			k1 = n;
			k2= 0;
			write(*,*) "interpolation out of range (right)";
			return;
	else
	k=0;
		do i = 1 , n
			if ( x > x_grid(2**( n-i ) + k) ) then
				k = k+2**(n-i);
			endif
		enddo
	k1=k;
	k2=k+1;
!testing
	!write(*,*) k1;
	!write(*,*) k2;
	endif

end subroutine findinterval2n

!!!! PRIMITIVE FUNCTION (real)
subroutine Primint(dx,fx,N_x,Ifx) !the function is stored in field fx, it computes Ifx by trapezoidal rule, N_x is length of the grid
real*8, intent(in) :: dx;
real*8, dimension (:), intent(in) :: fx;
integer, intent(in) :: N_x;
real*8, dimension (size (fx)), intent(out) :: Ifx;
integer :: k;

Ifx(1)=0.0d0;
do k = 2, N_x
	Ifx(k)=Ifx(k-1) + 0.5d0*(fx(k)+fx(k-1))*dx
enddo
 
end subroutine Primint


!!!! PRIMITIVE FUNCTION (real)
subroutine Primint_part(x,fx,N_x,Ifx) !the function is stored in field fx, it computes Ifx by trapezoidal rule, N_x is length of the grid, an arbitrary interval partition
real*8, dimension (:), intent(in) :: x;
real*8, dimension (:), intent(in) :: fx;
integer, intent(in) :: N_x;
real*8, dimension (size (fx)), intent(out) :: Ifx;
integer :: k;

Ifx(1)=0.0d0;
do k = 2, N_x
	Ifx(k)=Ifx(k-1) + 0.5d0*(fx(k)+fx(k-1))*(x(k)-x(k-1))
enddo
 
end subroutine Primint_part

!%%%%%%%%%%% Bessel J0(x)
FUNCTION besselj0(x)
  !IMPLICIT NONE
  REAL*8, INTENT(IN) :: x;
  REAL*8 :: besselj0,y,inter1,inter2;
  REAL*8 :: ax,xx,z;
  REAL*8, DIMENSION(5) :: p,q;
  REAL*8, DIMENSION(6) :: r,s;
  INTEGER :: k;

  p(1) = 1.0d0; p(2) = -0.1098628627d-2; p(3) = 0.2734510407d-4; p(4) = -0.2073370639d-5; p(5) = 0.2093887211d-6;
  q(1) = -0.1562499995d-1; q(2) = 0.1430488765d-3; q(3) = -0.6911147651d-5; q(4) = 0.7621095161d-6; q(5) = -0.934945152d-7;

  r(1) = 57568490574.0d0; r(2) = -13362590354.0d0; r(3) = 651619640.7d0; r(4) = -11214424.18d0;
  r(5) = 77392.33017d0; r(6) = -184.9052456d0;

  s(1) = 57568490411.0d0; s(2) = 1029532985.0d0; s(3) = 9494680.718d0; s(4) = 59272.64853d0;
  s(5) = 267.8532712d0; s(6) = 1.0d0;

  if (abs(x) < 8.0) then !Direct rational function fit.
   y=x**2.0d0
   inter1 = r(6); inter2 = s(6);
   do k = 1 , 5
     inter1 = inter1*y + r(6-k);
     inter2 = inter2*y + s(6-k);
   enddo 
   besselj0=inter1/inter2;
  else !Fitting function (6.5.9).
   ax=dabs(x)
   z=8.0d0/ax
   y=z**2.0d0
   xx=ax-0.785398164d0;

   inter1 = p(5); inter2 = q(5);
   do k = 1 , 4
     inter1 = inter1*y + p(5-k);
     inter2 = inter2*y + q(5-k);
   enddo 
   besselj0=dsqrt(0.636619772d0/ax)*(dcos(xx)*inter1-z*dsin(xx)*inter2);
  end if

  !besselj0= 1.0d0;
 
END FUNCTION besselj0


end module libraries
