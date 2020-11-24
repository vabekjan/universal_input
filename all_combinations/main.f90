
!%%%%%%%%%%%%%%%%%  Program  %%%%%%%%%%%%%%
PROGRAM makelist
!This program makes a list of all posible configurations of input paramaters, the first column is varying the fatest.
!Input file structure (each row for one parameter): "minimal value", "maximal value", "# of INTERMEDIATE steps = N" (i.e. total # of steps is (N+2) including boundary values)
!Special situation of not varying parameter is given by # of points (-1) only the MAXIMAL value is then taken.


use libraries;

  IMPLICIT NONE

  character(*), parameter :: driving_file = "multiparam.inp"
  character(*), parameter :: output_file = "list_of_combinations.dat"

  real*8, dimension(:,:), Allocatable :: values;
  real*8, dimension(:), Allocatable :: val_min,val_max;
  integer, dimension(:), Allocatable :: n_drive,setup;
  integer :: N_par,N_tot,N_dum;
  real*8 :: step;


  !loops & file reading
  integer :: k1,k2,k3,k4;

 character(255) :: cwd,dum_w;

  
  !N = 150; !# of points (this includes val_max/min values, i.e. set N=M-1 for #of inputs = M)
   
  !val_min = -0.09d0;
  !val_max = 0.09d0;

!!! LOAD ALL IN INITIAL PARAMETERS
	cwd=TRIM(driving_file);
	N_par = filelength(cwd);
	allocate(n_drive(1:N_par)); allocate(val_min(1:N_par)); allocate(val_max(1:N_par));
	
	open(unit=1, file=driving_file,form="FORMATTED",action='read')
	open(UNIT=2,FILE="n_drive.dat",FORM="FORMATTED",action='write');
	do k1 = 1, N_par
		read(unit=1,fmt=*) val_min(k1), val_max(k1), n_drive(k1);
		n_drive(k1)=n_drive(k1) + 2;
		write(UNIT=2,fmt='(i5)') n_drive(k1);
	enddo

	close(1); close(2);

	! N_tot total number of paramaeters combination is the product of all param posibilities
	N_tot = 1;
	do k1 = 1, N_par
		N_tot = N_tot*(n_drive(k1)); 
	enddo
!write(*,*) "n_drive=", n_drive;
!write(*,*) "val_min=", val_min;
!write(*,*) "val_max=", val_max;


!!! PROCEDURE  

	N_dum=MAXVAL(n_drive)
!write(*,*) "N_dum=", N_dum;
	allocate(values(N_par,N_dum))
	do k1 = 1 , N_par
		
		if ( n_drive(k1) > 0 ) then
			step = (val_max(k1)-val_min(k1))/dfloat(n_drive(k1) - 1);
			do k2 = 0 , (n_drive(k1) - 1)
				values(k1,k2+1) = val_min(k1) + dfloat(k2)*step;			
			enddo
		endif
		values(k1,n_drive(k1)) = val_max(k1)
	enddo
!write(*,*) "values=";
!write(*,*) values(1,1);
!write(*,*) values(1,2);
!write(*,*) values(1,3);
!write(*,*) values(1,4);
!write(*,*) values(1,5);
!write(*,*) values(2,1);
!write(*,*) values(2,2);
!write(*,*) values(2,3);
!write(*,*) values(2,4);
!write(*,*) values(2,5);


write(*,*) n_drive;
	open(UNIT=1,FILE=output_file,FORM="FORMATTED",action='write');
	open(UNIT=2,FILE="values.txt",FORM="FORMATTED",action='write');
	allocate(setup(1:N_par));
	do k1 = 1, N_par
		setup(k1)=1;
	enddo
    
	do k1 = 1 , N_tot !setup is an array that indexes actual values of parameters to write, it's defined in the increase procedure
	write(UNIT=2,fmt='(e12.6,X)',advance='no') dfloat(k1);
write(*,*) setup;

		do k2 = 1, (N_par-1)
			write(UNIT=1,fmt='(e12.6,X)',advance='no') values(k2,setup(k2));
		enddo
		write(UNIT=1,fmt='(e12.6)') values(k2,setup(N_par));
		if ( .not. (k1 == N_tot ) ) then
			call increase(1,n_drive,setup);
		endif
	  
	
	enddo

  close(1); close(2);

END PROGRAM makelist