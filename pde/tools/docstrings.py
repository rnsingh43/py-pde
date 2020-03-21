'''
Created on Mar 21, 2020

.. codeauthor:: David Zwicker <david.zwicker@ds.mpg.de>
'''

import textwrap
import re
from typing import TypeVar



DOCSTRING_REPLACEMENTS = {
    # description of function arguments
    '{ARG_BOUNDARIES_INSTANCE}': """
        Specifies the boundary conditions applied to the field. This must be an
        instance of :class:`~pde.grids.boundaries.axes.Boundaries`, which can be
        created from various data formats using the class method
       :func:`~pde.grids.boundaries.axes.Boundaries.from_data`."""[1:],
       
    '{ARG_BOUNDARIES}': """
        The boundary conditions applied to the field. In the most general 
        format, this is a list with boundary conditions for each axis. If a 
        particular axis is periodic, only periodic boundary conditions are
        allowed (indicated by the string 'periodic'). For non-periodic axes,
        different boundary conditions can be specified for the lower and upper
        end of the axis (generally a tuple of two conditions). Typical choices 
        for individual conditions are Dirichlet conditions that enforce a value
        NUM (specified by `{'value': NUM}`) and Neumann conditions that enforce 
        the value DERIV for the derivative in the normal direction (specified by
        `{'derivative': DERIV}`). If both sides of an axis have the same 
        boundary condition, only one needs to be specified (instead of the 
        tuple). Similarly, if all axes have the same boundary conditions, only 
        one axis needs to be specified (instead of the list). Finally, the 
        special value 'natural' imposes periodic boundary conditions for 
        periodic axis and a vanishing derivative otherwise."""[1:],
    
    '{ARG_TRACKER_INTERVAL}': """
        Determines how often the tracker interrupts the simulation. Simple
        numbers are interpreted as durations measured in the simulation time
        variable. Alternatively, a string using the format 'hh:mm:ss' can be
        used to give durations in real time. Finally, instances of the classes
        defined in :mod:`~pde.trackers.intervals` can be given for more control.
        """[1:-1],
        
    '{ARG_PLOT_QUANTITIES}': """
        A list of quantities that are shown side by side. If `quantities` is a
        simple list, the panels will be rendered as a single row, while a 2d
        list allows for multiple rows.
        Each panel is defined by a dictionary, where the item with key 'source'
        is mandatory, since it defines what is being shown. The value associated
        with 'source' can be either an integer specifying the component that is
        shown or a function which is evaluated with the full state as input.
        Additional items in the dictionary are 'title' (setting the title of the
        panel), 'scale' (defining the color range shown; these are typically two
        numbers defining the lower and upper bound, but if only one is given the
        range [0, scale] is assumed), and 'cmap' (defining the colormap being
        used)."""[1:],
        
    # descriptions of the discretization and the symmetries         
    '{DESCR_CYLINDRICAL_GRID}': r"""
        The cylindrical grid assumes polar symmetry, so that fields only depend
        on the radial coordinate `r` and the axial coordinate `z`. Here, the
        first axis is along the radius, while the second axis is along the axis
        of the cylinder. The radial discretization is defined as
        :math:`r_i = (i + \frac12) \Delta r` for :math:`i=0, \ldots, N_r-1`.
        """[1:-1],
        
    '{DESCR_POLAR_GRID}': r"""
        The polar grid assumes polar symmetry, so that fields only depend on the
        radial coordinate `r`. The radial discretization is defined as
        :math:`r_i = r_\mathrm{min} + (i + \frac12) \Delta r` for
        :math:`i=0, \ldots, N_r-1`,  where :math:`r_\mathrm{min}` is the radius
        of the inner boundary, which is zero by default. Note that the radius of
        the outer boundary is given by
        :math:`r_\mathrm{max} = r_\mathrm{min} + N_r \Delta r`."""[1:],
        
    '{DESCR_SPHERICAL_GRID}': r"""
        The spherical grid assumes spherical symmetry, so that fields only
        depend on the radial coordinate `r`. The radial discretization is
        defined as :math:`r_i = r_\mathrm{min} + (i + \frac12) \Delta r` for
        :math:`i=0, \ldots, N_r-1`,  where :math:`r_\mathrm{min}` is the radius
        of the inner boundary, which is zero by default. Note that the radius of
        the outer boundary is given by
        :math:`r_\mathrm{max} = r_\mathrm{min} + N_r \Delta r`."""[1:]
}



TFunc = TypeVar('TFunc')


def fill_in_docstring(f: TFunc) -> TFunc:
    """ decorator that replaces text in the docstring of a function """
    # initialize textwrapper for formatting docstring
    tw = textwrap.TextWrapper(width=80, expand_tabs=True,
                              replace_whitespace=True, drop_whitespace=True)
            
    docstring = f.__doc__
    for token, value in DOCSTRING_REPLACEMENTS.items():
        
        def repl(matchobj) -> str:
            """ helper function replacing token in docstring """
            tw.initial_indent = tw.subsequent_indent = matchobj.group(1)
            return tw.fill(textwrap.dedent(value))

        # replace the token with the correct indentation
        docstring = re.sub(f"^([ \t]*){token}", repl, docstring,  # type: ignore
                           flags=re.MULTILINE)

    f.__doc__ = docstring
    return f