module libraries

IMPLICIT NONE;

CONTAINS

recursive subroutine increase(k,n_drive,setup) !!! No exception handling, i.e. a correct input has to be used
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

end module libraries